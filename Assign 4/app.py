import os
from flask import Flask, render_template, request, url_for, redirect, flash, session
from werkzeug.security import check_password_hash
from models import db, Person, Item, Order, OrderLine,  Inventory, WeightedVeggie, PackVeggie, UnitPriceVeggie,PremadeBox # 从 models 中导入 db 和其他模型

from datetime import datetime

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

# View vegetables and premade boxes
@app.route('/view_vegetables')
def view_vegetables():
    if 'user_id' not in session or session.get('role') != 'customer':
        flash('Please log in as a customer.', 'warning')
        return redirect(url_for('login'))
    
        
    # Query items and join relevant tables
    items = (
        db.session.query(Item)
        .outerjoin(WeightedVeggie, Item.id == WeightedVeggie.id)
        .outerjoin(PackVeggie, Item.id == PackVeggie.id)
        .outerjoin(UnitPriceVeggie, Item.id == UnitPriceVeggie.id)
        .all()
    )

    if 'cart' not in session:
        session['cart'] = []
    cart = session['cart']
    total_price = sum(item['line_total'] for item in cart) if cart else 0

     # Get the cart from session, or an empty list if it doesn't exist


  

    return render_template('view_vegetables.html', items=items, cart=cart, total_price=total_price)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'user_id' not in session:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login'))

    # Get item_id and quantity from the form data
    item_id = request.form.get('item_id')
    quantity = int(request.form.get('quantity', 0))

    # Debugging output
    print(f"Received item_id: {item_id}, quantity: {quantity}")

    # Retrieve the item from the database
    item = Item.query.get(item_id)

    # Handle missing or incorrect items
    if not item:
        print("Item not found!")
        flash('Item not found!', 'danger')
        return redirect(url_for('view_vegetables'))

    # Handle stock shortages
    if item.inventory.quantity < quantity:
        print(f"Insufficient stock! Available: {item.inventory.quantity}, Requested: {quantity}")
        flash('Insufficient stock!', 'danger')
        return redirect(url_for('view_vegetables'))

    # Initialize the cart if it's not already in the session
    if 'cart' not in session:
        session['cart'] = []

    cart = session['cart']

    # Check if the item is already in the cart
    item_in_cart = next((cart_item for cart_item in cart if cart_item['item_id'] == int(item_id)), None)
    
    if item_in_cart:
        # Update quantity and line total if item already exists in the cart
        item_in_cart['quantity'] += quantity
        item_in_cart['line_total'] = item.calculate_total(item_in_cart['quantity'])
        print(f"Updated item in cart: {item_in_cart}")
    else:
        # Add new item to the cart
        new_cart_item = {
            'item_id': int(item_id),  # Cast to int for consistency
            'name': item.name,
            'price': item.get_price(),
            'quantity': quantity,
            'line_total': item.calculate_total(quantity)
        }
        cart.append(new_cart_item)
        print(f"Added new item to cart: {new_cart_item}")
    
    # Update the session with the modified cart
    session['cart'] = cart

    # Debug output to check the updated session data
    print(f"Session cart updated: {session['cart']}")

    flash(f'{item.name} added to your cart!', 'success')
    return redirect(url_for('view_vegetables'))


@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    # 检查用户是否已登录
    if 'user_id' not in session:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login'))

    # 获取要删除的 item_id
    item_id = int(request.form.get('item_id'))

    # 初始化购物车（如果没有则创建空列表）
    if 'cart' not in session:
        session['cart'] = []

    cart = session['cart']

    # 过滤掉要删除的商品
    session['cart'] = [item for item in cart if item['item_id'] != item_id]

    # 更新后的购物车
    print(f"Updated cart after removal: {session['cart']}")

    flash('Item removed from cart', 'success')
    return redirect(url_for('view_vegetables'))


@app.route('/customize_premade_box/<int:box_id>', methods=['GET', 'POST'])
def customize_premade_box(box_id):
    box = PremadeBox.query.get(box_id)
    max_content = box.max_content
    

    items = (
        db.session.query(Item)
        .filter(Item.type != 'premade_box')
        .join(Inventory)
        .filter(Inventory.quantity > 0)
        .all()
    )
    
    if request.method == 'POST':
        selected_items = request.form.getlist('selected_items')
        quantities = request.form.getlist('quantity')

        # 计算用户选择的总蔬菜数量
        total_quantity = sum(int(q) for q in quantities)

        if total_quantity > max_content:
            flash(f"Total items exceed the box limit! Maximum allowed: {max_content}", "danger")
            return redirect(url_for('customize_premade_box', box_id=box_id))

        # 如果数量合法，进行处理（保存数据或进行下一步）
        # 保存逻辑（依赖于项目的特定处理逻辑）

        flash('Premade Box customized successfully!', 'success')
        return redirect(url_for('view_vegetables'))

    return render_template('customize_premade_box.html', items=items, box=box)

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