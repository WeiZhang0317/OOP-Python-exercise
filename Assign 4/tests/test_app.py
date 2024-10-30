# pytest tests/test_app.py --cov=app --cov-report=term-missing


import pytest,random
from flask import session, url_for
from app import app, db
from models import Customer, Item, Inventory, PremadeBox, Order, Person,CorporateCustomer,Veggie,PackVeggie,WeightedVeggie,UnitPriceVeggie
from werkzeug.security import generate_password_hash

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
        db.session.remove()
        db.drop_all()


def login(client, username="testuser", password="password"):
    return client.post(url_for('login'), data=dict(username=username, password=password), follow_redirects=True)

# Test cover page
def test_coverpage(client):
    response = client.get(url_for('coverpage'))
    assert response.status_code == 200

# Test login and session
def test_login(client):
    response = login(client)
    assert b'Login successful!' in response.data
    assert 'user_id' in session
    assert 'role' in session

def test_login_invalid(client):
    response = client.post(url_for('login'), data=dict(username="wronguser", password="wrongpassword"), follow_redirects=True)
    assert b'Incorrect username or password' in response.data
    assert 'user_id' not in session

# Test logout
def test_logout(client):
    login(client)
    response = client.get(url_for('logout'), follow_redirects=True)
    assert b'You have been successfully logged out.' in response.data
    assert 'user_id' not in session

# Test vegetable viewing
def test_view_vegetables(client):
    login(client)
    response = client.get(url_for('view_vegetables'))
    assert response.status_code == 200

def test_view_vegetables_not_logged_in(client):
    response = client.get(url_for('view_vegetables'), follow_redirects=True)
    assert b'Please log in as a customer or staff.' in response.data

# Test adding to cart
def test_add_to_cart(client):
    login(client)
    item = Item.query.first()
    response = client.post(url_for('add_to_cart'), data=dict(item_id=item.id, quantity=3), follow_redirects=True)
    assert b'added to your cart!' in response.data
    assert session['cart'][0]['name'] == "Carrot"

def test_add_to_cart_insufficient_stock(client):
    login(client)
    item = Item.query.first()
    Inventory.query.filter_by(item_id=item.id).update({"quantity": 0})
    db.session.commit()
    response = client.post(url_for('add_to_cart'), data=dict(item_id=item.id, quantity=3), follow_redirects=True)
    assert b'Insufficient stock!' in response.data

# Test removing from cart
def test_remove_from_cart(client):
    login(client)
    item = Item.query.first()
    client.post(url_for('add_to_cart'), data=dict(item_id=item.id, quantity=3), follow_redirects=True)
    response = client.post(url_for('remove_from_cart'), data=dict(item_id=item.id), follow_redirects=True)
    assert b'Item removed from cart' in response.data
    assert len(session['cart']) == 0

# Test checkout
def test_checkout(client):
    login(client)
    item = Item.query.first()
    client.post(url_for('add_to_cart'), data=dict(item_id=item.id, quantity=2), follow_redirects=True)
    response = client.post(url_for('checkout'), follow_redirects=True)
    assert b'created successfully' in response.data

def test_checkout_empty_cart(client):
    login(client)
    response = client.post(url_for('checkout'), follow_redirects=True)
    assert b'Your cart is empty!' in response.data

# Test payment page
def test_payment_page(client):
    login(client)
    order = Order(order_number="ORD123", customer_id=1, total_cost=50.0)
    db.session.add(order)
    db.session.commit()
    response = client.get(url_for('payment_page', order_id=order.id))
    assert response.status_code == 200

# Test payment processing
def test_process_payment(client):
    login(client)
    order = Order(order_number="ORD123", customer_id=1, total_cost=20.0)
    db.session.add(order)
    db.session.commit()
    response = client.post(url_for('process_payment', order_id=order.id), data={
        'delivery_option': 'standard',
        'payment_method': 'credit_card',
        'card_number': '4111111111111111',
        'card_expiry_date': '12/25',
        'cvv': '123'
    }, follow_redirects=True)
    assert b'Payment processed successfully!' in response.data

def test_process_payment_invalid_method(client):
    login(client)
    order = Order(order_number="ORD123", customer_id=1, total_cost=20.0)
    db.session.add(order)
    db.session.commit()
    response = client.post(url_for('process_payment', order_id=order.id), data={
        'delivery_option': 'standard',
        'payment_method': 'invalid_method'
    }, follow_redirects=True)
    assert b'Payment failed' in response.data

# Test order cancellation
def test_cancel_order(client):
    login(client)
    order = Order(order_number="ORD123", customer_id=1, total_cost=20.0)
    db.session.add(order)
    db.session.commit()
    response = client.post(url_for('cancel_order', order_id=order.id), follow_redirects=True)
    assert b'Order has been canceled.' in response.data

# Test customize premade box
def test_customize_premade_box(client):
    login(client)
    box = PremadeBox.query.first()
    response = client.get(url_for('customize_premade_box', box_id=box.id))
    assert response.status_code == 200
    response = client.post(url_for('customize_premade_box', box_id=box.id), data={
        'quantity_1': 3  # Assuming item with id=1 in test data
    }, follow_redirects=True)
    assert b'Items added to your premade box successfully!' in response.data
