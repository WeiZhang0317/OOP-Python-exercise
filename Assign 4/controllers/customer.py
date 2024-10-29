from flask import Blueprint, render_template, redirect, request, flash, session, url_for
from models import Customer, CorporateCustomer, Order, OrderStatus, db
from service.report import SalesReportService

customer_blueprint = Blueprint('customer', __name__, url_prefix='/customer')


@customer_blueprint.route("/list", methods=['GET'])
def customer_list():
    """Render a list of all customers."""
    items = Customer.query.all()
    return render_template('customer/customer_list.html', **locals())


@customer_blueprint.route("/detail/<customer_id>", methods=['GET'])
def customer_detail(customer_id):
    """Render details for a specific customer, including weekly, monthly, and yearly sales."""
    item = Customer.query.get(customer_id)
    weekly_sales = SalesReportService.get_weekly_sales(customer_id)
    monthly_sales = SalesReportService.get_monthly_sales(customer_id)
    yearly_sales = SalesReportService.get_yearly_sales(customer_id)
    return render_template('customer/detail.html', **locals())


@customer_blueprint.route("/corporate/list", methods=['GET'])
def corporate_customer_list():
    """Render a list of all corporate customers."""
    items = CorporateCustomer.query.all()
    return render_template('customer/corporate_list.html', **locals())


@customer_blueprint.route("/corporate/detail/<customer_id>", methods=['GET'])
def corporate_customer_detail(customer_id):
    """Render details for a specific corporate customer, including weekly, monthly, and yearly sales."""
    item = CorporateCustomer.query.get(customer_id)
    weekly_sales = SalesReportService.get_weekly_sales(customer_id)
    monthly_sales = SalesReportService.get_monthly_sales(customer_id)
    yearly_sales = SalesReportService.get_yearly_sales(customer_id)
    return render_template('customer/corporate_detail.html', **locals())


@customer_blueprint.route('/history_orders', methods=['GET'])
def history_orders():
    """Retrieve all past orders for the currently logged-in user and display details."""
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))

    # Retrieve all orders belonging to the current user
    items = Order.query.filter_by(customer_id=user_id).all()  # Filter by customer_id instead of user_id
    return render_template('customer/history_orders.html', **locals())


@customer_blueprint.route('/detail/<order_id>', methods=['GET'])
def detail(order_id):
    """Retrieve details of a specific order for the current user."""
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))

    # Retrieve the order and ensure it belongs to the current user
    item = Order.query.filter_by(id=order_id, customer_id=user_id).first()  # Filter by customer_id
    if not item:
        flash('Order not found or you do not have permission to view this order.', 'danger')
        return redirect(url_for('customer.current_orders'))

    return render_template('customer/detail.html', **locals())


@customer_blueprint.route("/profile", methods=['GET'])
def customer_profile():
    """Retrieve and display the profile of the current user."""
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))
    
    # Query for the customer's profile information
    customer = db.session.query(Customer).filter_by(cust_id=user_id).first()
    if not customer:
        flash("User information not found.", "warning")
        return redirect(url_for('login'))

    # Render the profile template with customer information
    return render_template('customer/profile.html', customer=customer)
