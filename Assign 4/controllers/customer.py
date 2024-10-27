from flask import Blueprint, render_template, redirect, request
from models import Customer, CorporateCustomer
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
