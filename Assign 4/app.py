import os
from flask import Flask, render_template, request, url_for, redirect, flash, session
from werkzeug.security import check_password_hash
from models import db, Person, Customer, CorporateCustomer, Item, Order,Cart,OrderStatus, OrderLine,DebitCardPayment,  Inventory, WeightedVeggie, PackVeggie, UnitPriceVeggie,PremadeBox,CreditCardPayment # 从 models 中导入 db 和其他模型
from datetime import datetime
from service import PremadeBoxService
from sqlalchemy.orm import aliased
import re
from sqlalchemy.orm import joinedload

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

    weighted_veggie_alias = aliased(WeightedVeggie)
    pack_veggie_alias = aliased(PackVeggie)
    unit_price_veggie_alias = aliased(UnitPriceVeggie)
    premade_box_alias = aliased(PremadeBox)

    items = (
        db.session.query(Item)
        .outerjoin(weighted_veggie_alias, Item.id == weighted_veggie_alias.id)
        .outerjoin(pack_veggie_alias, Item.id == pack_veggie_alias.id)
        .outerjoin(unit_price_veggie_alias, Item.id == unit_price_veggie_alias.id)
        .outerjoin(premade_box_alias, Item.id == premade_box_alias.id)
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
    item = db.session.get(Item, item_id)
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




@app.route('/checkout', methods=['POST'])
def checkout():
    if 'user_id' not in session:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login'))

     # 获取当前用户，可能是私人客户或公司客户
    customer = db.session.query(Customer).filter_by(cust_id=session['user_id']).first()

    # 检查客户是否可以下订单（基于客户类型）
    if isinstance(customer, CorporateCustomer):
        if not customer.can_place_order():
            flash('Your corporate balance is below the required minimum, you cannot place an order.', 'danger')
            return redirect(url_for('view_vegetables'))
    else:
        if not customer.can_place_order():
            flash('Your personal balance exceeds the allowed limit, you cannot place an order.', 'danger')
            return redirect(url_for('view_vegetables'))

    # 打印确认可以下单
    print("Check done: customer can place order")
    
    # 获取当前购物车
    cart = Cart(session.get('cart'))
    if not cart or len(cart.get_cart()) == 0:
        flash('Your cart is empty!', 'warning')
        return redirect(url_for('view_vegetables'))

    # 获取当前用户ID
    customer_id = session.get('user_id')

    # 获取staff_id，可以通过session 或者默认分配
    staff_id = session.get('staff_id', 4)  # 默认分配给staff_id 4

    # 创建一个新的订单，使用 generate_unique_order_number() 生成唯一订单号
    order = Order(
        order_number=Order.generate_unique_order_number(),
        customer_id=customer_id,
        staff_id=staff_id,
        order_status=OrderStatus.PENDING.value,
        total_cost=cart.get_total_price()
    )

    # 将订单添加到数据库
    db.session.add(order)
    db.session.flush()  # 获取订单ID
    session['current_order_id'] = order.id

    # 为购物车中的每个商品创建相应的 OrderLine 记录并减少库存
    for cart_item in cart.get_cart():
        # 查找对应商品的库存记录
        inventory = db.session.query(Inventory).filter_by(item_id=cart_item['item_id']).first()
        if inventory:
            # 减少库存
            try:
                inventory.reduce_stock(cart_item['quantity'])
            except ValueError as e:
                flash(f'Error: {str(e)} for item {cart_item["name"]}', 'danger')
                return redirect(url_for('view_vegetables'))

            # 创建订单项
            order_line = OrderLine(
                order_id=order.id,  # 使用刚创建的订单ID
                item_id=cart_item['item_id'],
                quantity=cart_item['quantity'],
                line_total=cart_item['line_total']
            )
            db.session.add(order_line)
        else:
            flash(f'No inventory found for item {cart_item["name"]}', 'danger')
            return redirect(url_for('view_vegetables'))

    # 最后提交事务，将订单和订单项保存到数据库，并更新库存
    db.session.commit()

    # 清空购物车
    session['cart'] = []
    # 跳转到支付页面并传递订单ID
    flash(f'Order {order.id} created successfully. Please proceed to payment.', 'success')

    return redirect(url_for('process_payment', order_id=order.id))


@app.route('/process_payment', methods=['GET', 'POST'])
def process_payment():
    order_id = request.args.get('order_id')
    customer = db.session.query(Customer).filter_by(cust_id=session['user_id']).first()
    order = db.session.query(Order).filter_by(id=order_id, customer_id=customer.cust_id).first()

    if not order:
        flash('Order not found.', 'danger')
        return redirect(url_for('view_vegetables'))
    
    # 在GET请求中获取订单的所有order_lines及其关联的item信息
    if request.method == 'GET':
        order_lines = order.get_order_lines()

    if request.method == 'POST':
        delivery_option = request.form.get('delivery_option')
        payment_method = request.form.get('payment_method')
        card_number = request.form.get('card_number')
        card_expiry_date = request.form.get('card_expiry_date')
        cvv = request.form.get('cvv')
        payment_amount = order.calculate_total_with_delivery(delivery_option)



        if payment_method == 'credit_card':
            try:
                CreditCardPayment.validate_credit_card(card_number, card_expiry_date, cvv)
                CreditCardPayment.create_payment(customer, card_number, request.form.get('card_type'), card_expiry_date, payment_amount)
            except ValueError as e:
                flash(str(e), 'danger')
                return redirect(url_for('process_payment', order_id=order_id))
        
        elif payment_method == 'debit_card':
            bank_name = request.form.get('bank_name')
            if not re.fullmatch(r'\d{16}', card_number):
                flash("Invalid debit card number. It must be 16 digits.", 'danger')
                return redirect(url_for('process_payment', order_id=order_id))
            DebitCardPayment.create_payment(customer, bank_name, card_number, payment_amount)

        # 更新订单状态
        order.update_status('Paid')
        flash('Payment processed successfully!', 'success')
        return redirect(url_for('view_vegetables'))

    return render_template('payment.html', customer=customer, order_id=order_id, order=order, order_lines=order_lines)


@app.route('/cancel_order/<int:order_id>', methods=['POST'])
def cancel_order(order_id):
    customer = db.session.query(Customer).filter_by(cust_id=session['user_id']).first()
    order = db.session.query(Order).filter_by(id=order_id, customer_id=customer.cust_id).first()

    if order:
        order.update_status('Canceled')
        flash('Order has been canceled.', 'info')
    else:
        flash('Order not found.', 'danger')

    return redirect(url_for('view_vegetables'))



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





# 启动应用
if __name__ == '__main__':
    app.run(debug=True)