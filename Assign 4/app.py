import os
from flask import Flask, render_template, request, url_for, redirect, flash, session
from werkzeug.security import check_password_hash
from models import db, Person, Item, Order,Cart, OrderLine,  Inventory, WeightedVeggie, PackVeggie, UnitPriceVeggie,PremadeBox # 从 models 中导入 db 和其他模型
from datetime import datetime
from service import PremadeBoxService

basedir = os.path.abspath(os.path.dirname(__file__))

# 初始化 Flask 应用
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/fresh_harvest12'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

# 初始化数据库
db.init_app(app)

# 创建数据库表
with app.app_context():
    db.create_all()

# 首页路由
@app.route('/')
def coverpage():
    return render_template('coverpage.html')

# 登录路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 根据用户名查找用户
        person = Person.query.filter_by(username=username).first()

        if person and check_password_hash(person._Person__password, password):  # 验证密码
            session['user_id'] = person.id  # 将用户 ID 存入 session
            session['role'] = person.role  # 假设有 role 属性
            flash('登录成功！', 'success')
            return redirect(url_for('dashboard'))
       
        else:
            flash('用户名或密码错误，请重试。', 'danger')

    return render_template('login.html')

# 注销路由
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    flash('你已成功注销。', 'info')
    return redirect(url_for('login'))



# #######################
# # Customer-related routes
# #######################

# Customer Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('请登录以访问控制面板。', 'warning')
        return redirect(url_for('login'))

    # 根据用户角色显示不同的内容
    if session.get('role') == 'customer':
        items = Item.query.all()  # 客户查看商品
        return render_template('dashboard.html', items=items, role='customer')

    elif session.get('role') == 'staff':
        orders = Order.query.all()  # 员工管理订单
        return render_template('dashboard.html', orders=orders, role='staff')

    else:
        flash('未授权的访问。', 'danger')
        return redirect(url_for('login'))

@app.route('/view_vegetables')
def view_vegetables():
    if 'user_id' not in session or session.get('role') != 'customer':
        flash('Please log in as a customer.', 'warning')
        return redirect(url_for('login'))

    # 获取商品列表
    items = (
        db.session.query(Item)
        .outerjoin(WeightedVeggie, Item.id == WeightedVeggie.id)
        .outerjoin(PackVeggie, Item.id == PackVeggie.id)
        .outerjoin(UnitPriceVeggie, Item.id == UnitPriceVeggie.id)
        .outerjoin(PremadeBox, Item.id ==PremadeBox.id)
        .all()
    )

    # 获取购物车对象并计算总价
    cart = Cart(session.get('cart'))
    total_price = cart.get_total_price()

    return render_template('view_vegetables.html', items=items, cart=cart.get_cart(), total_price=total_price)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'user_id' not in session:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login'))

    # 获取商品ID和数量
    item_id = request.form.get('item_id')
    quantity = int(request.form.get('quantity', 0))

    # 从数据库中获取商品
    item = Item.query.get(item_id)
    if not item:
        flash('Item not found!', 'danger')
        return redirect(url_for('view_vegetables'))

    # 检查库存
    if item.inventory.quantity < quantity:
        flash('Insufficient stock!', 'danger')
        return redirect(url_for('view_vegetables'))

    # 获取购物车对象
    cart = Cart(session.get('cart'))
    
     # 打印购物车内容进行调试
    print("Cart content: ", cart.get_cart())

    # 添加商品到购物车
    cart.add_item(item, quantity)

    # 更新session
    session['cart'] = cart.get_cart()
    flash(f'{item.name} added to your cart!', 'success')

    return redirect(url_for('view_vegetables'))


@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    if 'user_id' not in session:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login'))

    # 获取要删除的商品ID
    item_id = int(request.form.get('item_id'))

    # 获取购物车对象
    cart = Cart(session.get('cart'))

    # 从购物车移除商品
    cart.remove_item(item_id)

    # 更新session
    session['cart'] = cart.get_cart()
    flash('Item removed from cart', 'success')

    return redirect(url_for('view_vegetables'))

def clean_premade_box_items():
    if 'premade_box' in session:
        session['premade_box']['items'] = [
            item for item in session['premade_box']['items']
            if item.get('item_id') and item.get('name')
        ]

@app.route('/customize_premade_box/<int:box_id>', methods=['GET', 'POST'])
def customize_premade_box(box_id):
    box = db.session.get(PremadeBox, box_id)

    if not box:
        flash('Premade Box not found.', 'danger')
        return redirect(url_for('view_vegetables'))

    # Get available veggies to add to the premade box
    items = (
        db.session.query(Item)
        .filter(Item.type != 'premade_box')  # Exclude premade boxes
        .join(Inventory)
        .filter(Inventory.quantity > 0)  # Only show items in stock
        .all()
    )

    # Store selected items
    selected_items = []

    if request.method == 'POST':
        # Process form data for veggie selection
        total_selected_quantity = 0
        for item in items:
            quantity = int(request.form.get(f'quantity_{item.id}', 0))
            if quantity > 0:
                total_selected_quantity += quantity
                selected_items.append({
                    'item_id': item.id,
                    'name': item.name,
                    'quantity': quantity
                })

        # Check box capacity
        if total_selected_quantity > box.max_content:
            flash(f"Total items exceed the box limit! Maximum allowed: {box.max_content}.", 'danger')
            return redirect(url_for('customize_premade_box', box_id=box_id))

        flash('Items added to your premade box successfully!', 'success')

    return render_template('customize_premade_box.html', items=items, box=box, selected_items=selected_items)



@app.route('/remove_from_premade_box', methods=['POST'])
def remove_from_premade_box():
    if 'user_id' not in session:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login'))

    # 打印删除前的session内容
    print("Before removing, session['premade_box']['items']:", session.get('premade_box', {}).get('items', []))
    
    # 清理空的 item（没有 item_id 或 name）
    if 'premade_box' in session:
        session['premade_box']['items'] = [
            item for item in session['premade_box']['items']
            if item.get('item_id') and item.get('name')
        ]
        print("After cleaning empty items, session['premade_box']['items']:", session['premade_box']['items'])

    # 获取要删除的商品ID
    item_id_str = request.form.get('item_id')
    item_id = int(item_id_str) if item_id_str and item_id_str.isdigit() else None
    item_name = request.form.get('item_name')

    # 打印删除前的item_id和item_name
    print(f"Item ID to remove: {item_id}, Item Name to remove: {item_name}")

    # 使用服务层来处理删除逻辑
    if item_id:
        PremadeBoxService.remove_item_from_box(session, item_id)
        print(f"Item with ID {item_id} removed.")
    elif item_name:
        PremadeBoxService.remove_item_by_name(session, item_name)
        print(f"Item with name {item_name} removed.")
    else:
        flash('Invalid item data. Cannot remove item.', 'danger')
        return redirect(url_for('customize_premade_box', box_id=request.form.get('box_id')))

    # 打印删除后的session内容
    print("After removing, session['premade_box']['items']:", session['premade_box']['items'])

    flash('Item removed from Premade Box', 'success')
    return redirect(url_for('customize_premade_box', box_id=request.form.get('box_id')))

# @app.route('/checkout', methods=['GET', 'POST'])
# def checkout():
#     if 'user_id' not in session:
#         flash('Please log in to continue!', 'warning')
#         return redirect(url_for('login'))

#     if 'cart' not in session or len(session['cart']) == 0:
#         flash('Your cart is empty, please add some items first.', 'warning')
#         return redirect(url_for('view_vegetables'))

#     # Create a new order for the customer
#     order = Order(
#         order_number=generate_order_number(),
#         customer_id=session['user_id'],
#         staff_id=1,  # Assuming 1 is the default staff handling the order
#         order_status=OrderStatus.PENDING.value,
#         total_cost=0
#     )
#     db.session.add(order)
#     db.session.commit()

#     total_cost = 0
#     for cart_item in session['cart']:
#         item = Item.query.get(cart_item['item_id'])
#         if item and item.inventory.quantity >= cart_item['quantity']:
#             # Create an order line and add it to the order
#             line_total = item.calculate_total(cart_item['quantity'])
#             order_line = OrderLine(order_id=order.id, item_id=item.id, quantity=cart_item['quantity'], line_total=line_total)
#             db.session.add(order_line)

#             # Reduce inventory
#             item.inventory.reduce_stock(cart_item['quantity'])
#             total_cost += line_total
#         else:
#             flash(f'Insufficient stock for {cart_item["name"]}.', 'danger')
#             return redirect(url_for('view_vegetables'))

#     # Update the order with the total cost
#     order.total_cost = total_cost
#     db.session.commit()

#     # Clear the cart after successful checkout
#     session.pop('cart', None)

#     flash('Your order was successfully placed!', 'success')
#     return redirect(url_for('dashboard'))

# # Add items to cart
# @app.route('/customer/add_to_cart/<int:item_id>', methods=['POST'])
# def add_to_cart(item_id):
#     quantity = int(request.form.get('quantity'))
    
#     cart = session.get('cart', [])
#     cart.append({'item_id': item_id, 'quantity': quantity})
#     session['cart'] = cart
#     flash('Item added to cart!', 'success')
    
#     return redirect(url_for('view_vegetables'))


# # View cart and checkout
# @app.route('/customer/cart')
# def cart():
#     if 'cart' not in session or not session['cart']:
#         flash('Your cart is empty.', 'warning')
#         return redirect(url_for('view_vegetables'))
    
#     cart_items = []
#     total_price = 0
#     for cart_item in session['cart']:
#         item = Item.query.get(cart_item['item_id'])
#         total_price += item.price * cart_item['quantity']
#         cart_items.append({'item': item, 'quantity': cart_item['quantity']})
    
#     return render_template('customer/cart.html', cart_items=cart_items, total_price=total_price)


# # Checkout
# @app.route('/customer/checkout', methods=['POST'])
# def checkout():
#     customer_id = session['user_id']
#     cart = session.get('cart', [])
    
#     if not cart:
#         flash('Your cart is empty.', 'warning')
#         return redirect(url_for('view_vegetables'))

#     # Create an order
#     order = Order(customer_id=customer_id, total_cost=0, order_date=datetime.now(), order_status='pending')
#     db.session.add(order)
#     db.session.commit()

#     total_price = 0
#     for cart_item in cart:
#         item = Item.query.get(cart_item['item_id'])
#         line_total = item.price * cart_item['quantity']
#         total_price += line_total

#         order_line = OrderLine(order_id=order.id, item_id=item.id, quantity=cart_item['quantity'], line_total=line_total)
#         db.session.add(order_line)
    
#     # Update the order total cost
#     order.total_cost = total_price
#     db.session.commit()
    
#     session.pop('cart', None)
#     flash('Order placed successfully!', 'success')
    
#     return redirect(url_for('customer_dashboard'))


# #######################
# # Staff-related routes
# #######################

# Staff Dashboard



# # View all vegetables and premade boxes
# @app.route('/staff/view_all_vegetables')
# def view_all_vegetables():
#     if 'user_id' not in session or session.get('role') != 'staff':
#         flash('Please log in as staff to view this page.', 'warning')
#         return redirect(url_for('login'))
    
#     items = Item.query.all()
#     return render_template('staff/view_all_vegetables.html', items=items)


# # View current orders
# @app.route('/staff/current_orders')
# def current_orders():
#     if 'user_id' not in session or session.get('role') != 'staff':
#         flash('Please log in as staff to view this page.', 'warning')
#         return redirect(url_for('login'))
    
#     orders = Order.query.filter_by(order_status='pending').all()
#     return render_template('staff/current_orders.html', orders=orders)


# # Update order status
# @app.route('/staff/update_order/<int:order_id>', methods=['POST'])
# def update_order(order_id):
#     new_status = request.form.get('order_status')
#     order = Order.query.get(order_id)
#     order.order_status = new_status
#     db.session.commit()

#     flash('Order status updated successfully!', 'success')
#     return redirect(url_for('current_orders'))



# 启动应用
if __name__ == '__main__':
    app.run(debug=True)