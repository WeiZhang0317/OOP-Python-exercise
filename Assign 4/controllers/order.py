from flask import Blueprint, render_template, request, flash, redirect, url_for

from models import db
from models.order import Order, OrderStatus
from service.report import SalesReportService, PopularItemReportService

order_blueprint = Blueprint('order', __name__, url_prefix='/order')


@order_blueprint.route('/current_orders', methods=['GET'])
def current_orders():
    """
    查询所有当前订单及其详细信息
    """
    items = Order.query.filter(Order.order_status.notin_([OrderStatus.CANCELED.value])).all()
    return render_template('order/current_orders.html', items=items, OrderStatus=OrderStatus)


@order_blueprint.route('/history_orders', methods=['GET'])
def history_orders():
    """
    查询所有历史订单及其详细信息
    """
    items = Order.query.all()
    return render_template('order/history_orders.html', **locals())


@order_blueprint.route('/detail/<order_id>', methods=['GET'])
def detail(order_id):
    item = Order.query.get(order_id)
    return render_template('order/detail.html', **locals())


@order_blueprint.route('/update_status/<order_id>', methods=['GET'])
def update_status(order_id):
    """
    变更状态
    """
    order = Order.query.get(order_id)
    next_status = OrderStatus.get_next_status(order.order_status)
    if next_status:
        order.set_order_status(next_status)
        db.session.commit()
    return redirect(url_for('order.current_orders'))


@order_blueprint.route('/sales_report', methods=['GET'])
def sales_report():
    """
    生成一周，一个月和一年的总销售额
    """
    weekly = SalesReportService.get_weekly_sales()
    monthly = SalesReportService.get_monthly_sales()
    yearly = SalesReportService.get_yearly_sales()

    popularInfo = PopularItemReportService.get_popular_items_summary()
    leastPopularInfo = PopularItemReportService.get_least_popular_items_summary()
    return render_template('order/sales_report.html', **locals())


