from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from models.item import Item
from models.order import Order, OrderLine
from models.customer import Customer

customer_blueprint = Blueprint('customer', __name__)

# 客户首页（Dashboard）
@customer_blueprint.route('/dashboard')
def dashboard():
    if 'user_id' not in session or session.get('role') != 'customer':
        flash('Please log in as a customer to access the dashboard.', 'warning')
        return redirect(url_for('login'))
    
    # 展示可购买的蔬菜和预制箱
    items = Item.query.all()
    return render_template('customer/dashboard.html', items=items)


# 查看蔬菜和预制箱页面
@customer_blueprint.route('/view_vegetables')
def view_vegetables():
    if 'user_id' not in session or session.get('role') != 'customer':
        flash('Please log in as a customer.', 'warning')
        return redirect(url_for('login'))
    
    items = Item.query.all()
    return render_template('customer/view_vegetables.html', items=items)


# 添加商品到购物车
@customer_blueprint.route('/add_to_cart/<int:item_id>', methods=['POST'])
def add_to_cart(item_id):
    quantity = int(request.form.get('quantity'))
    
    # 假设session中存放着购物车信息
    cart = session.get('cart', [])
    cart.append({'item_id': item_id, 'quantity': quantity})
    session['cart'] = cart
    flash('Item added to cart!', 'success')
    
    return redirect(url_for('customer.view_vegetables'))


# 购物车查看及结算
@customer_blueprint.route('/cart')
def cart():
    if 'cart' not in session or not session['cart']:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('customer.view_vegetables'))
    
    # 查询购物车中的商品详细信息
    cart_items = []
    total_price = 0
    for cart_item in session['cart']:
        item = Item.query.get(cart_item['item_id'])
        total_price += item.price * cart_item['quantity']
        cart_items.append({'item': item, 'quantity': cart_item['quantity']})
    
    return render_template('customer/cart.html', cart_items=cart_items, total_price=total_price)


# 结账
@customer_blueprint.route('/checkout', methods=['POST'])
def checkout():
    # 假设用户已登录
    customer_id = session['user_id']
    cart = session.get('cart', [])
    
    if not cart:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('customer.view_vegetables'))

    # 创建订单
    order = Order(customer_id=customer_id, total_cost=0)
    db.session.add(order)
    db.session.commit()

    total_price = 0
    for cart_item in cart:
        item = Item.query.get(cart_item['item_id'])
        line_total = item.price * cart_item['quantity']
        total_price += line_total

        order_line = OrderLine(order_id=order.id, item_id=item.id, quantity=cart_item['quantity'], line_total=line_total)
        db.session.add(order_line)
    
    # 更新订单总价
    order.total_cost = total_price
    db.session.commit()
    
    # 清空购物车
    session.pop('cart', None)
    flash('Order placed successfully!', 'success')
    
    return redirect(url_for('customer.dashboard'))
