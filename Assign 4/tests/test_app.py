# tests/test_app.py

import pytest
from flask import session, url_for
from app import app, db
from models import Customer, Item, Inventory, PremadeBox, Order, Person
from werkzeug.security import generate_password_hash

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Set up test data
            hashed_password = generate_password_hash("password")
            person = Person(username="testuser", role="customer", _Person__password=hashed_password)
            customer = Customer(cust_id=1, username="testuser", cust_balance=100.0)
            item = Item(name="Carrot", price=2.0)
            inventory = Inventory(item_id=item.id, quantity=100)
            premade_box = PremadeBox(name="Veggie Box", max_content=10)
            db.session.add_all([person, customer, item, inventory, premade_box])
            db.session.commit()
            yield client
        db.session.remove()
        db.drop_all()

def login(client, username="testuser", password="password"):
    return client.post(url_for('login'), data=dict(username=username, password=password), follow_redirects=True)

def test_coverpage(client):
    """Test that the cover page loads successfully."""
    response = client.get(url_for('coverpage'))
    assert response.status_code == 200

def test_login(client):
    """Test login functionality and session creation."""
    response = login(client)
    assert b'Login successful!' in response.data
    assert 'user_id' in session
    assert 'role' in session

def test_logout(client):
    """Test logout functionality and session clearing."""
    login(client)
    response = client.get(url_for('logout'), follow_redirects=True)
    assert b'You have been successfully logged out.' in response.data
    assert 'user_id' not in session

def test_view_vegetables(client):
    """Test vegetable viewing page loads correctly."""
    login(client)
    response = client.get(url_for('view_vegetables'))
    assert response.status_code == 200

def test_add_to_cart(client):
    """Test adding an item to the cart."""
    login(client)
    item = Item.query.first()
    response = client.post(url_for('add_to_cart'), data=dict(item_id=item.id, quantity=3), follow_redirects=True)
    assert b'added to your cart!' in response.data
    assert session['cart'][0]['name'] == "Carrot"

def test_remove_from_cart(client):
    """Test removing an item from the cart."""
    login(client)
    item = Item.query.first()
    client.post(url_for('add_to_cart'), data=dict(item_id=item.id, quantity=3), follow_redirects=True)
    response = client.post(url_for('remove_from_cart'), data=dict(item_id=item.id), follow_redirects=True)
    assert b'Item removed from cart' in response.data
    assert len(session['cart']) == 0

def test_checkout(client):
    """Test checkout process initiates an order."""
    login(client)
    item = Item.query.first()
    client.post(url_for('add_to_cart'), data=dict(item_id=item.id, quantity=2), follow_redirects=True)
    response = client.post(url_for('checkout'), follow_redirects=True)
    assert b'created successfully' in response.data

def test_payment_page(client):
    """Test accessing the payment page."""
    login(client)
    order = Order(order_number="ORD123", customer_id=1, total_cost=50.0)
    db.session.add(order)
    db.session.commit()
    response = client.get(url_for('payment_page', order_id=order.id))
    assert response.status_code == 200

def test_process_payment(client):
    """Test payment processing functionality."""
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

def test_cancel_order(client):
    """Test order cancellation."""
    login(client)
    order = Order(order_number="ORD123", customer_id=1, total_cost=20.0)
    db.session.add(order)
    db.session.commit()
    response = client.post(url_for('cancel_order', order_id=order.id), follow_redirects=True)
    assert b'Order has been canceled.' in response.data

def test_customize_premade_box(client):
    """Test customization of premade boxes."""
    login(client)
    box = PremadeBox.query.first()
    response = client.get(url_for('customize_premade_box', box_id=box.id))
    assert response.status_code == 200
    response = client.post(url_for('customize_premade_box', box_id=box.id), data={
        'quantity_1': 3  # Assuming item with id=1 in test data
    }, follow_redirects=True)
    assert b'Items added to your premade box successfully!' in response.data
