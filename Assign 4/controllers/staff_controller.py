from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from models.order import Order
from models.item import Item
from models.customer import Customer

staff_blueprint = Blueprint('staff', __name__)

# 员工Dashboard
@staff_blueprint.route('/dashboard')
def dashboard():
    if 'user_id' not in session or session.get('role') != 'staff':
        flash('Please log in as staff to access the dashboard.', 'warning')
        return redirect(url_for('login'))
    
    return render_template('staff/dashboard.html')


# 查看所有蔬菜和预制箱
@staff_blueprint.route('/view_all_vegetables')
def view_all_vegetables():
    if 'user_id' not in session or session.get('role') != 'staff':
        flash('Please log in as staff to view this page.', 'warning')
        return redirect(url_for('login'))
    
    items = Item.query.all()
    return render_template('staff/view_all_vegetables.html', items=items)


# 查看当前订单
@staff_blueprint.route('/current_orders')
def current_orders():
    if 'user_id' not in session or session.get('role') != 'staff':
        flash('Please log in as staff to view this page.', 'warning')
        return redirect(url_for('login'))
    
    orders = Order.query.filter_by(order_status='pending').all()
    return render_template('staff/current_orders.html', orders=orders)


# 更新订单状态
@staff_blueprint.route('/update_order/<int:order_id>', methods=['POST'])
def update_order(order_id):
    new_status = request.form.get('order_status')
    order = Order.query.get(order_id)
    order.order_status = new_status
    db.session.commit()

    flash('Order status updated successfully!', 'success')
    return redirect(url_for('staff.current_orders'))
