import os
from flask import Flask, render_template, request, url_for, redirect, flash, session
from werkzeug.security import check_password_hash
from models import db, Person, Customer, CorporateCustomer, Item, Order, Cart, OrderStatus, OrderLine, DebitCardPayment, Inventory, WeightedVeggie, PackVeggie, UnitPriceVeggie, PremadeBox, CreditCardPayment
from controllers import init_controller
from sqlalchemy.orm import aliased



# Set the base directory path for the application
basedir = os.path.abspath(os.path.dirname(__file__))

# Initialize the Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/fresh_harvest12'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize the database with Flask application context
db.init_app(app)

# Create all database tables if they do not exist
with app.app_context():
    db.create_all()


# #######################
# Shared routes, including browsing vegetables and placing orders and paying, etc are in app.py.
# For staff view order/customer see in controllers file
# #######################



# Route for the cover page
@app.route('/')
def coverpage():
    return render_template('coverpage.html')

# Route for login page handling both GET and POST requests
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Query the database for the user by username
        person = Person.query.filter_by(username=username).first()

        # Verify user and password, and set session variables upon successful login
        if person and check_password_hash(person._Person__password, password):
            session['user_id'] = person.id  # Store user ID in session
            session['role'] = person.role  # Store user role in session, if available
            flash('Login successful!', 'success')
            return redirect(url_for('view_vegetables'))

        else:
            flash('Incorrect username or password. Please try again.', 'danger')

    return render_template('login.html')

# Route to handle user logout, clearing session information
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    flash('You have been successfully logged out.', 'info')
    return redirect(url_for('login'))



@app.route('/view_vegetables')
def view_vegetables():
    # Ensure user is logged in; redirect to login page if not
    if 'user_id' not in session:
        flash('Please log in as a customer or staff.', 'warning')
        return redirect(url_for('login'))

    # Aliases for each vegetable type model for efficient querying
    weighted_veggie_alias = aliased(WeightedVeggie)
    pack_veggie_alias = aliased(PackVeggie)
    unit_price_veggie_alias = aliased(UnitPriceVeggie)
    premade_box_alias = aliased(PremadeBox)

    # Query to retrieve all items, joining different vegetable types if available
    items = (
        db.session.query(Item)
        .outerjoin(weighted_veggie_alias, Item.id == weighted_veggie_alias.id)
        .outerjoin(pack_veggie_alias, Item.id == pack_veggie_alias.id)
        .outerjoin(unit_price_veggie_alias, Item.id == unit_price_veggie_alias.id)
        .outerjoin(premade_box_alias, Item.id == premade_box_alias.id)
        .all()
    )

    # Retrieve customer list for staff role; create cart instance and calculate total price
    customer_list = Customer.get_all_customers() if session.get('role') == 'staff' else None
    cart = Cart(session.get('cart'))
    total_price = cart.get_total_price()

    return render_template('purchase/view_vegetables.html', items=items, customer_list=customer_list, cart=cart.get_cart(), total_price=total_price)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    # Ensure user is logged in before adding items
    if 'user_id' not in session:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login'))

    # Retrieve item ID and quantity from form data
    item_id = request.form.get('item_id')
    quantity = int(request.form.get('quantity', 0))

    # Fetch item from database based on item ID
    item = db.session.get(Item, item_id)
    if not item:
        flash('Item not found!', 'danger')
        return redirect(url_for('view_vegetables'))

    # Check if sufficient stock is available
    if not item.inventory.check_stock(quantity):
        flash('Insufficient stock!', 'danger')
        return redirect(url_for('view_vegetables'))

    # Initialize cart object from session data
    cart = Cart(session.get('cart'))

    # Debug: print cart contents for troubleshooting
    print("Cart content: ", cart.get_cart())

    # Add item and specified quantity to cart
    cart.add_item(item, quantity)

    # Update session with modified cart data
    session['cart'] = cart.get_cart()
    flash(f'{item.name} added to your cart!', 'success')

    return redirect(url_for('view_vegetables'))

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    # Ensure user is logged in before removing items
    if 'user_id' not in session:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login'))

    # Retrieve item ID of item to remove from form data
    item_id = int(request.form.get('item_id'))

    # Initialize cart object from session data
    cart = Cart(session.get('cart'))

    # Remove specified item from cart by item ID
    cart.remove_item(item_id)

    # Update session with modified cart data
    session['cart'] = cart.get_cart()
    flash('Item removed from cart', 'success')

    return redirect(url_for('view_vegetables'))

@app.route('/checkout', methods=['POST'])
def checkout():
    # Ensure the user is logged in; redirect if not
    if 'user_id' not in session:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login'))
    
    # Set customer_id and staff_id based on the user's role
    if session.get('role') == 'customer':
        customer_id = session.get('user_id')  # Customer uses their own ID
        staff_id = 5  # Default staff ID

        # Try to get the CorporateCustomer instance to check ordering permissions
        corporate_customer = CorporateCustomer.query.get(customer_id)
        if corporate_customer and not corporate_customer.can_place_order():
            # Corporate customer cannot place order due to insufficient balance
            flash("Corporate customer cannot place an order due to insufficient balance.", 'danger')
            return redirect(url_for('view_vegetables'))
        
        # Retrieve Customer instance and verify balance
        customer = db.session.query(Customer).filter_by(cust_id=customer_id).first()
        if not customer:
            flash(f"Customer with ID {customer_id} not found.", 'danger')
            return redirect(url_for('view_vegetables'))
        elif not customer.can_place_order_based_on_balance():
            flash("Your balance is insufficient to place an order.", 'danger')
            return redirect(url_for('view_vegetables'))
      
    else:
        # For staff, get customer_id from the form data
        customer_id = request.form.get('customer_id')
        if not customer_id:
            flash("Please select a customer for placing the order.", 'warning')
            return redirect(url_for('view_vegetables'))
        
        staff_id = session.get('user_id')
        
        # Attempt to retrieve CorporateCustomer instance and validate balance
        corporate_customer = CorporateCustomer.query.get(customer_id)
        if corporate_customer:
            if not corporate_customer.can_place_order():
                flash("Corporate customer cannot place an order due to insufficient balance.", 'danger')
                return redirect(url_for('view_vegetables'))
        else:
            # If not a corporate customer, retrieve Customer instance and check balance
            customer = db.session.query(Customer).filter_by(cust_id=customer_id).first()
            if not customer:
                flash(f"Customer with ID {customer_id} not found.", 'danger')
                return redirect(url_for('view_vegetables'))
            elif not customer.can_place_order_based_on_balance():
                flash("Customer's balance is insufficient to place an order.", 'danger')
                return redirect(url_for('view_vegetables'))
    
    # Retrieve cart object and check if it contains any items
    cart = Cart(session.get('cart'))
    if not cart or len(cart.get_cart()) == 0:
        flash('Your cart is empty!', 'warning')
        return redirect(url_for('view_vegetables'))
    
    # Create a new order instance
    order = Order(
        order_number=Order.generate_unique_order_number(),
        customer_id=customer_id,
        staff_id=staff_id,
        order_status=OrderStatus.PENDING.value,
        total_cost=cart.get_total_price()
    )

    # Add the order to the database and get order ID
    db.session.add(order)
    db.session.flush()  # Retrieve order ID for further processing
    session['current_order_id'] = order.id

    # For each item in the cart, create an OrderLine record and reduce inventory
    for cart_item in cart.get_cart():
        inventory = db.session.query(Inventory).filter_by(item_id=cart_item['item_id']).first()
        if inventory:
            try:
                inventory.reduce_stock(cart_item['quantity'])
            except ValueError as e:
                # Handle stock reduction errors
                flash(f'Error: {str(e)} for item {cart_item["name"]}', 'danger')
                return redirect(url_for('view_vegetables'))

            # Create an order line for each item in the cart
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

    # Commit the transaction and clear the cart
    db.session.commit()
    session['cart'] = []

    flash(f'Order {order.id} created successfully. Please proceed to payment.', 'success')
    return redirect(url_for('current_order', order_id=order.id))

@app.route('/current_order/<int:order_id>', methods=['GET'])
def current_order(order_id):
    # Query order and fetch customer information
    order = db.session.query(Order).filter_by(id=order_id).first()
    if not order:
        flash('Order not found.', 'danger')
        return redirect(url_for('view_vegetables'))

    customer = db.session.query(Customer).filter_by(cust_id=order.customer_id).first()
    if not customer:
        flash("Customer details not found for this order.", 'danger')
        return redirect(url_for('view_vegetables'))

    # Retrieve order lines associated with this order
    order_lines = order.get_order_lines()
    return render_template('purchase/current_order.html', customer=customer, order_id=order_id, order=order, order_lines=order_lines)


# Route to display the delivery and payment options form
@app.route('/payment/<int:order_id>', methods=['GET'])
def payment_page(order_id):
    customer = db.session.query(Customer).filter_by(cust_id=session['user_id']).first()
    order = db.session.query(Order).filter_by(id=order_id, customer_id=customer.cust_id).first()

    if not order:
        flash('Order not found.', 'danger')
        return redirect(url_for('view_vegetables'))

    return render_template('purchase/payment.html', customer=customer, order_id=order_id, order=order)


# Route to handle payment processing
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
    
    # Calculate total cost with delivery option if selected
    payment_amount = order.calculate_total_with_delivery(delivery_option)

    try:
        # Process payment based on selected method
        if payment_method == 'credit_card':
            card_type = request.form.get('card_type')
            CreditCardPayment.validate_credit_card(card_number, card_expiry_date, cvv)
            CreditCardPayment.create_payment(customer, card_number, card_type, card_expiry_date, payment_amount)

        elif payment_method == 'debit_card':
            bank_name = request.form.get('bank_name')
            DebitCardPayment.validate_debit_card(card_number)
            DebitCardPayment.create_payment(customer, bank_name, card_number, payment_amount)
            
        elif payment_method == 'account_balance':
            # Attempt to deduct from customer's account balance
            if customer.deduct_balance(payment_amount):
                db.session.commit()  # Commit transaction if deduction succeeds
                flash("Payment deducted from your account balance!", "success")
            else:
                flash("Payment failed: Outstanding balance exceeds the maximum allowed debt limit.", "danger")
                return redirect(url_for('payment_page', order_id=order_id))

        # Update order status to 'Paid' upon successful payment
        order.update_status('Paid')
        flash('Payment processed successfully!', 'success')
        return redirect(url_for('view_vegetables'))

    except ValueError as e:
        flash(str(e), 'danger')
        return redirect(url_for('payment_page', order_id=order_id))


# Route to cancel an order
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


if __name__ == '__main__':
    app.run(debug=True)