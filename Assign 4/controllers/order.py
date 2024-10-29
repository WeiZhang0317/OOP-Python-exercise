from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import db
from models.order import Order, OrderStatus
from service.report import SalesReportService, PopularItemReportService

order_blueprint = Blueprint('order', __name__, url_prefix='/order')


@order_blueprint.route('/current_orders', methods=['GET'])
def current_orders():
    """Query and display all current orders excluding canceled ones."""
    items = Order.query.filter(Order.order_status.notin_([OrderStatus.CANCELED.value])).all()
    return render_template('order/current_orders.html', items=items, OrderStatus=OrderStatus)


@order_blueprint.route('/history_orders', methods=['GET'])
def history_orders():
    """Query and display all past orders with their details."""
    items = Order.query.all()
    return render_template('order/history_orders.html', **locals())


@order_blueprint.route('/detail/<order_id>', methods=['GET'])
def detail(order_id):
    """Display the details of a specific order based on order_id."""
    item = Order.query.get(order_id)
    return render_template('order/detail.html', **locals())


@order_blueprint.route('/update_status/<order_id>', methods=['GET'])
def update_status(order_id):
    """Change the status of an order to its next logical status."""
    order = Order.query.get(order_id)
    next_status = OrderStatus.get_next_status(order.order_status)
    if next_status:
        order.set_order_status(next_status)
        db.session.commit()
    return redirect(url_for('order.current_orders'))


@order_blueprint.route('/sales_report', methods=['GET'])
def sales_report():
    """Generate and display sales reports for weekly, monthly, and yearly totals."""
    weekly = SalesReportService.get_weekly_sales()
    monthly = SalesReportService.get_monthly_sales()
    yearly = SalesReportService.get_yearly_sales()

    # Retrieve popular and least popular items for summary display
    popularInfo = PopularItemReportService.get_popular_items_summary()
    leastPopularInfo = PopularItemReportService.get_least_popular_items_summary()
    return render_template('order/sales_report.html', **locals())
