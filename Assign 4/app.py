import os
from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from models.person import Person
from models.item import Item
from models.order import Order, OrderLine
from werkzeug.security import check_password_hash
from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@localhost:3306/fresh_harvest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)

# Home route
@app.route('/')
def coverpage():
    return render_template('coverpage.html')


# Sign-in Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Find the person in the database by username
        person = Person.query.filter_by(username=username).first()

        if person and check_password_hash(person.password, password):
            session['user_id'] = person.id  # Store the user ID in session
            session['role'] = person.role  # Assuming Person model has a role attribute
            flash('Login successful!', 'success')
            if person.role == 'customer':
                return redirect(url_for('customer_dashboard'))
            elif person.role == 'staff':
                return redirect(url_for('staff_dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('login.html')


# Logout Route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


#######################
# Customer-related routes
#######################

# Customer Dashboard
@app.route('/customer/dashboard')
def customer_dashboard():
    if 'user_id' not in session or session.get('role') != 'customer':
        flash('Please log in as a customer to access the dashboard.', 'warning')
        return redirect(url_for('login'))
    
    items = Item.query.all()
    return render_template('customer/dashboard.html', items=items)


# View vegetables and premade boxes
@app.route('/customer/view_vegetables')
def view_vegetables():
    if 'user_id' not in session or session.get('role') != 'customer':
        flash('Please log in as a customer.', 'warning')
        return redirect(url_for('login'))
    
    items = Item.query.all()
    return render_template('customer/view_vegetables.html', items=items)


# Add items to cart
@app.route('/customer/add_to_cart/<int:item_id>', methods=['POST'])
def add_to_cart(item_id):
    quantity = int(request.form.get('quantity'))
    
    cart = session.get('cart', [])
    cart.append({'item_id': item_id, 'quantity': quantity})
    session['cart'] = cart
    flash('Item added to cart!', 'success')
    
    return redirect(url_for('view_vegetables'))


# View cart and checkout
@app.route('/customer/cart')
def cart():
    if 'cart' not in session or not session['cart']:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('view_vegetables'))
    
    cart_items = []
    total_price = 0
    for cart_item in session['cart']:
        item = Item.query.get(cart_item['item_id'])
        total_price += item.price * cart_item['quantity']
        cart_items.append({'item': item, 'quantity': cart_item['quantity']})
    
    return render_template('customer/cart.html', cart_items=cart_items, total_price=total_price)


# Checkout
@app.route('/customer/checkout', methods=['POST'])
def checkout():
    customer_id = session['user_id']
    cart = session.get('cart', [])
    
    if not cart:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('view_vegetables'))

    # Create an order
    order = Order(customer_id=customer_id, total_cost=0, order_date=datetime.now(), order_status='pending')
    db.session.add(order)
    db.session.commit()

    total_price = 0
    for cart_item in cart:
        item = Item.query.get(cart_item['item_id'])
        line_total = item.price * cart_item['quantity']
        total_price += line_total

        order_line = OrderLine(order_id=order.id, item_id=item.id, quantity=cart_item['quantity'], line_total=line_total)
        db.session.add(order_line)
    
    # Update the order total cost
    order.total_cost = total_price
    db.session.commit()
    
    session.pop('cart', None)
    flash('Order placed successfully!', 'success')
    
    return redirect(url_for('customer_dashboard'))


#######################
# Staff-related routes
#######################

# Staff Dashboard
@app.route('/staff/dashboard')
def staff_dashboard():
    if 'user_id' not in session or session.get('role') != 'staff':
        flash('Please log in as staff to access the dashboard.', 'warning')
        return redirect(url_for('login'))
    
    return render_template('staff/dashboard.html')


# View all vegetables and premade boxes
@app.route('/staff/view_all_vegetables')
def view_all_vegetables():
    if 'user_id' not in session or session.get('role') != 'staff':
        flash('Please log in as staff to view this page.', 'warning')
        return redirect(url_for('login'))
    
    items = Item.query.all()
    return render_template('staff/view_all_vegetables.html', items=items)


# View current orders
@app.route('/staff/current_orders')
def current_orders():
    if 'user_id' not in session or session.get('role') != 'staff':
        flash('Please log in as staff to view this page.', 'warning')
        return redirect(url_for('login'))
    
    orders = Order.query.filter_by(order_status='pending').all()
    return render_template('staff/current_orders.html', orders=orders)


# Update order status
@app.route('/staff/update_order/<int:order_id>', methods=['POST'])
def update_order(order_id):
    new_status = request.form.get('order_status')
    order = Order.query.get(order_id)
    order.order_status = new_status
    db.session.commit()

    flash('Order status updated successfully!', 'success')
    return redirect(url_for('current_orders'))


if __name__ == '__main__':
    app.run(debug=True)
