import os
from flask import Flask, render_template, request, url_for, redirect, flash, session
from werkzeug.security import check_password_hash
from models import db, Person, Item, Order, OrderLine  # 从 models 中导入 db 和其他模型
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
            if person.role == 'customer':
                return redirect(url_for('coverpage'))
            elif person.role == 'staff':
                return redirect(url_for('coverpage'))
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

# 启动应用
if __name__ == '__main__':
    app.run(debug=True)


# #######################
# # Customer-related routes
# #######################

# # Customer Dashboard
# @app.route('/customer/dashboard')
# def customer_dashboard():
#     if 'user_id' not in session or session.get('role') != 'customer':
#         flash('Please log in as a customer to access the dashboard.', 'warning')
#         return redirect(url_for('login'))
    
#     items = Item.query.all()
#     return render_template('customer/dashboard.html', items=items)


# # View vegetables and premade boxes
# @app.route('/customer/view_vegetables')
# def view_vegetables():
#     if 'user_id' not in session or session.get('role') != 'customer':
#         flash('Please log in as a customer.', 'warning')
#         return redirect(url_for('login'))
    
#     items = Item.query.all()
#     return render_template('customer/view_vegetables.html', items=items)


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

# # Staff Dashboard
# @app.route('/staff/dashboard')
# def staff_dashboard():
#     if 'user_id' not in session or session.get('role') != 'staff':
#         flash('Please log in as staff to access the dashboard.', 'warning')
#         return redirect(url_for('login'))
    
#     return render_template('staff/dashboard.html')


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


# if __name__ == '__main__':
#     app.run(debug=True)
