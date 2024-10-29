import os
from flask import Flask, render_template, request, url_for, redirect, flash, session
from werkzeug.security import check_password_hash
from models import db, Person, Customer, CorporateCustomer, Item, Order,Cart,OrderStatus, OrderLine,DebitCardPayment,  Inventory, WeightedVeggie, PackVeggie, UnitPriceVeggie,PremadeBox,CreditCardPayment # 从 models 中导入 db 和其他模型
from controllers import init_controller
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
            return redirect(url_for('view_vegetables'))

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


@app.route('/view_vegetables')
def view_vegetables():
    if 'user_id' not in session:
        flash('Please log in as a customer or staff.', 'warning')
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
    customer_list = Customer.get_all_customers() if session.get('role') == 'staff' else None
    cart = Cart(session.get('cart'))
    total_price = cart.get_total_price()

    return render_template('purchase/view_vegetables.html', items=items, customer_list=customer_list, cart=cart.get_cart(), total_price=total_price)


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
    if not item.inventory.check_stock(quantity):
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
    
    # 判断用户角色并设置 customer_id 和 staff_id
    if session.get('role') == 'customer':
        customer_id = session.get('user_id')  # 客户使用自己的 ID
        staff_id = 5  # 默认员工 ID 为 5
          # 尝试直接获取 CorporateCustomer 实例
     
        corporate_customer = CorporateCustomer.query.get(customer_id)
        if corporate_customer and not corporate_customer.can_place_order():
            # 检查企业客户是否有权限下单
            flash("Corporate customer cannot place an order due to insufficient balance.", 'danger')
            return redirect(url_for('view_vegetables'))
        
        # 获取普通客户实例并进行余额验证
        customer = db.session.query(Customer).filter_by(cust_id=customer_id).first()
        if not customer:
            flash(f"Customer with ID {customer_id} not found.", 'danger')
            return redirect(url_for('view_vegetables'))
        elif not customer.can_place_order_based_on_balance():
            flash("Your balance is insufficient to place an order.", 'danger')
            return redirect(url_for('view_vegetables'))

      
    else:
        # staff 用户从表单获取 customer_id
        customer_id = request.form.get('customer_id')
        if not customer_id:
            flash("Please select a customer for placing the order.", 'warning')
            return redirect(url_for('view_vegetables'))
        
        staff_id = session.get('user_id')
        
          # 尝试直接获取 CorporateCustomer 实例
        corporate_customer = CorporateCustomer.query.get(customer_id)
        if corporate_customer:
            if not corporate_customer.can_place_order():
                flash("Corporate customer cannot place an order due to insufficient balance.", 'danger')
                return redirect(url_for('view_vegetables'))
        else:
            # 如果不是企业客户，获取普通客户实例
            customer = db.session.query(Customer).filter_by(cust_id=customer_id).first()
            if not customer:
                flash(f"Customer with ID {customer_id} not found.", 'danger')
                return redirect(url_for('view_vegetables'))
            elif not customer.can_place_order_based_on_balance():
                flash("Customer's balance is insufficient to place an order.", 'danger')
                return redirect(url_for('view_vegetables'))
    

        
    # 获取购物车对象
    cart = Cart(session.get('cart'))
    if not cart or len(cart.get_cart()) == 0:
        flash('Your cart is empty!', 'warning')
        return redirect(url_for('view_vegetables'))
    
 

    # 创建一个新的订单
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
        inventory = db.session.query(Inventory).filter_by(item_id=cart_item['item_id']).first()
        if inventory:
            try:
                inventory.reduce_stock(cart_item['quantity'])
            except ValueError as e:
                flash(f'Error: {str(e)} for item {cart_item["name"]}', 'danger')
                return redirect(url_for('view_vegetables'))

            # 创建订单项
            order_line = OrderLine(
                order_id=order.id,
                item_id=cart_item['item_id'],
                quantity=cart_item['quantity'],
                line_total=cart_item['line_total']
            )
            db.session.add(order_line)
        else:
            flash(f'No inventory found for item {cart_item["name"]}', 'danger')
            return redirect(url_for('view_vegetables'))

    # 提交事务并清空购物车
    db.session.commit()
    session['cart'] = []

    flash(f'Order {order.id} created successfully. Please proceed to payment.', 'success')
    return redirect(url_for('current_order', order_id=order.id))

@app.route('/current_order/<int:order_id>', methods=['GET'])
def current_order(order_id):
    # 查询订单并获取客户信息
    order = db.session.query(Order).filter_by(id=order_id).first()
    if not order:
        flash('Order not found.', 'danger')
        return redirect(url_for('view_vegetables'))

    customer = db.session.query(Customer).filter_by(cust_id=order.customer_id).first()
    if not customer:
        flash("Customer details not found for this order.", 'danger')
        return redirect(url_for('view_vegetables'))

    # 获取订单行
    order_lines = order.get_order_lines()
    return render_template('purchase/current_order.html', customer=customer, order_id=order_id, order=order, order_lines=order_lines)


# Route to handle the delivery option and payment method form
@app.route('/payment/<int:order_id>', methods=['GET'])
def payment_page(order_id):
    customer = db.session.query(Customer).filter_by(cust_id=session['user_id']).first()
    order = db.session.query(Order).filter_by(id=order_id, customer_id=customer.cust_id).first()

    if not order:
        flash('Order not found.', 'danger')
        return redirect(url_for('view_vegetables'))

    return render_template('purchase/payment.html', customer=customer, order_id=order_id, order=order)


# Route to process the payment
@app.route('/process_payment/<int:order_id>', methods=['POST'])
def process_payment(order_id):
    customer = db.session.query(Customer).filter_by(cust_id=session['user_id']).first()
    order = db.session.query(Order).filter_by(id=order_id, customer_id=customer.cust_id).first()

    if not order:
        flash('Order not found.', 'danger')
        return redirect(url_for('view_vegetables'))

    delivery_option = request.form.get('delivery_option')
    payment_method = request.form.get('payment_method')
    card_number = request.form.get('card_number')
    card_expiry_date = request.form.get('card_expiry_date')
    cvv = request.form.get('cvv')
    
    # Calculate total cost including delivery if applicable
    payment_amount = order.calculate_total_with_delivery(delivery_option)

    try:
        if payment_method == 'credit_card':
            card_type = request.form.get('card_type')
            CreditCardPayment.validate_credit_card(card_number, card_expiry_date, cvv)
            CreditCardPayment.create_payment(customer, card_number, card_type, card_expiry_date, payment_amount)


        elif payment_method == 'debit_card':
            bank_name = request.form.get('bank_name')        
            DebitCardPayment.validate_debit_card(card_number)               
            DebitCardPayment.create_payment(customer, bank_name, card_number, payment_amount)
            
        elif payment_method == 'account_balance':
            # Check if customer can process the payment from balance
            if customer.deduct_balance(payment_amount):
                # Deduct balance
                db.session.commit()
                flash("Payment deducted from your account balance!", "success")
            else:
                flash("Payment failed: Outstanding balance exceeds the maximum allowed debt limit.", "danger")
                return redirect(url_for('payment_page', order_id=order_id))

        # Update order status to "Paid"
        order.update_status('Paid')
        flash('Payment processed successfully!', 'success')
        return redirect(url_for('view_vegetables'))

    except ValueError as e:
        flash(str(e), 'danger')
        return redirect(url_for('payment_page', order_id=order_id))


# Route to handle order cancellation
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

    return render_template('purchase/customize_premade_box.html', items=items, box=box, selected_items=selected_items)



init_controller(app)

# 启动应用
if __name__ == '__main__':
    app.run(debug=True)