# python -m pytest -v tests/test_order_model.py

import pytest
from datetime import datetime
from models import db
from models.order import Order, OrderLine, OrderStatus, Cart
from models.customer import Customer
from models.item import Item
from app import app

@pytest.fixture
def setup_db():
    """Sets up the test client and database for testing."""
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

def test_cart_add_item(setup_db):
    """Test adding items to Cart and updating quantities."""
    item = Item(name="Apple", price=1.5)
    db.session.add(item)
    db.session.commit()

    cart = Cart(session_cart=[])
    cart.add_item(item, quantity=3)
    assert len(cart.get_cart()) == 1
    assert cart.get_cart()[0]['quantity'] == 3
    assert cart.get_total_price() == 4.5  # 1.5 * 3

    # Add the same item again, should update quantity
    cart.add_item(item, quantity=2)
    assert cart.get_cart()[0]['quantity'] == 5
    assert cart.get_total_price() == 7.5  # 1.5 * 5

def test_cart_remove_item(setup_db):
    """Test removing items from Cart."""
    item1 = Item(name="Orange", price=2.0)
    item2 = Item(name="Banana", price=1.0)
    db.session.add_all([item1, item2])
    db.session.commit()

    cart = Cart(session_cart=[])
    cart.add_item(item1, quantity=2)
    cart.add_item(item2, quantity=1)
    assert len(cart.get_cart()) == 2

    # Remove item1 from cart
    cart.remove_item(item_id=item1.id)
    assert len(cart.get_cart()) == 1
    assert cart.get_cart()[0]['name'] == "Banana"

def test_order_initialization(setup_db):
    """Test initializing an Order with customer and total cost."""
    customer = Customer(first_name="John", last_name="Doe", username="johndoe", password="password", cust_address="123 Main St")
    db.session.add(customer)
    db.session.commit()

    order = Order(order_number=Order.generate_unique_order_number(), customer_id=customer.cust_id, staff_id=1,
                  order_status=OrderStatus.PENDING.value, total_cost=50.0)
    db.session.add(order)
    db.session.commit()

    assert order.customer_id == customer.cust_id
    assert order.total_cost == 50.0
    assert order.order_status == OrderStatus.PENDING.value

def test_order_add_order_line(setup_db):
    """Test adding OrderLine to an Order."""
    customer = Customer(first_name="Jane", last_name="Smith", username="janesmith", password="secure", cust_address="456 Elm St")
    item = Item(name="Milk", price=2.5)
    db.session.add_all([customer, item])
    db.session.commit()

    order = Order(order_number=Order.generate_unique_order_number(), customer_id=customer.cust_id, staff_id=1,
                  order_status=OrderStatus.PENDING.value, total_cost=0.0)
    order_line = OrderLine(order_id=order.id, item_id=item.id, quantity=4, line_total=item.price * 4)
    
    order.add_order_line(order_line)
    db.session.add(order)
    db.session.commit()

    assert len(order.list_of_order_lines) == 1
    assert order.get_total_cost() == 10.0  # 2.5 * 4

def test_order_set_order_status(setup_db):
    """Test setting the order status using OrderStatus Enum."""
    order = Order(order_number=Order.generate_unique_order_number(), customer_id=1, staff_id=1,
                  order_status=OrderStatus.PENDING.value, total_cost=50.0)
    db.session.add(order)
    db.session.commit()

    order.set_order_status(OrderStatus.PAID.value)
    db.session.commit()
    assert order.order_status == OrderStatus.PAID.value

def test_order_generate_unique_order_number(setup_db):
    """Test generating a unique order number."""
    order1 = Order(order_number=Order.generate_unique_order_number(), customer_id=1, staff_id=1, order_status=OrderStatus.PENDING.value, total_cost=30.0)
    order2 = Order(order_number=Order.generate_unique_order_number(), customer_id=1, staff_id=1, order_status=OrderStatus.PENDING.value, total_cost=60.0)
    
    db.session.add_all([order1, order2])
    db.session.commit()

    assert order1.order_number != order2.order_number

def test_order_calculate_total_with_delivery(setup_db):
    """Test calculating total cost with optional delivery fee."""
    order = Order(order_number=Order.generate_unique_order_number(), customer_id=1, staff_id=1,
                  order_status=OrderStatus.PAID.value, total_cost=100.0)

    # Without delivery fee
    total_no_delivery = order.calculate_total_with_delivery(delivery_option='pickup')
    assert total_no_delivery == 100.0

    # With delivery fee
    total_with_delivery = order.calculate_total_with_delivery(delivery_option='delivery')
    assert total_with_delivery == 110.0  # 100.0 + 10.0 delivery fee

def test_order_line_get_line_total(setup_db):
    """Test calculating line total for an OrderLine."""
    item = Item(name="Bread", price=3.0)
    db.session.add(item)
    db.session.commit()

    order_line = OrderLine(order_id=1, item_id=item.id, quantity=5, line_total=15.0)
    assert order_line.get_line_total() == 15.0  # 3.0 * 5
