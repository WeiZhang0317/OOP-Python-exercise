from flask import Blueprint, render_template, redirect, request, flash, session,url_for
from models import Customer, CorporateCustomer,Order,OrderStatus,db
from service.report import SalesReportService

customer_blueprint = Blueprint('customer', __name__, url_prefix='/customer')


@customer_blueprint.route("/list", methods=['GET'])
def customer_list():
    items = Customer.query.all()
    return render_template('customer/customer_list.html', **locals())


@customer_blueprint.route("/detail/<customer_id>", methods=['GET'])
def customer_detail(customer_id):
    item = Customer.query.get(customer_id)
    weekly_sales = SalesReportService.get_weekly_sales(customer_id)
    monthly_sales = SalesReportService.get_monthly_sales(customer_id)
    yearly_sales = SalesReportService.get_yearly_sales(customer_id)
    return render_template('customer/detail.html', **locals())


@customer_blueprint.route("/corporate/list", methods=['GET'])
def corporate_customer_list():
    items = CorporateCustomer.query.all()
    return render_template('customer/corporate_list.html', **locals())


@customer_blueprint.route("/corporate/detail/<customer_id>", methods=['GET'])
def corporate_customer_detail(customer_id):
    item = CorporateCustomer.query.get(customer_id)
    weekly_sales = SalesReportService.get_weekly_sales(customer_id)
    monthly_sales = SalesReportService.get_monthly_sales(customer_id)
    yearly_sales = SalesReportService.get_yearly_sales(customer_id)
    return render_template('customer/corporate_detail.html', **locals())



@customer_blueprint.route('/history_orders', methods=['GET'])
def history_orders():
    """
    查询当前登录用户的所有历史订单及其详细信息
    """
    user_id = session.get('user_id')
    if not user_id:
        flash('请先登录。', 'warning')
        return redirect(url_for('login'))

    # 查询属于当前用户的所有订单
    items = Order.query.filter_by(customer_id=user_id).all()  # 使用 customer_id 而不是 user_id
    return render_template('customer/history_orders.html', **locals())

@customer_blueprint.route('/detail/<order_id>', methods=['GET'])
def detail(order_id):
    """
    查询当前用户的特定订单详细信息
    """
    user_id = session.get('user_id')
    if not user_id:
        flash('请先登录。', 'warning')
        return redirect(url_for('login'))

    # 查询订单并确保该订单属于当前用户
    item = Order.query.filter_by(id=order_id, customer_id=user_id).first()  # 使用 customer_id 进行过滤
    if not item:
        flash('订单不存在或无权限查看该订单。', 'danger')
        return redirect(url_for('customer.current_orders'))

    return render_template('customer/detail.html', **locals())

@customer_blueprint.route("/profile", methods=['GET'])
def customer_profile():
    # 从 session 获取用户 ID
    user_id = session.get('user_id')
    if not user_id:
        flash("请先登录。", "warning")
        return redirect(url_for('login'))
    
    # 查询当前用户的客户信息
    customer = db.session.query(Customer).filter_by(cust_id=user_id).first()
    if not customer:
        flash("未找到用户信息。", "warning")
        return redirect(url_for('login'))

    # 渲染模板，并传递客户信息
    return render_template('customer/profile.html', customer=customer)