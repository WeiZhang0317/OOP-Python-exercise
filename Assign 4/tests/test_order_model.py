# python -m pytest -v tests/test_order_model.py

import pytest
from models import db
from models.order import Cart,Order,OrderStatus
from models.item import Item
from app import app

# python -m pytest -v tests/test_order_model.py

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

def test_order_calculate_total_with_delivery(setup_db):
    """Test calculating total cost with optional delivery fee."""
    # Create a mock order
    order = Order(order_number=Order.generate_unique_order_number(), customer_id=1, staff_id=1,
                  order_status=OrderStatus.PAID.value, total_cost=100.0)

    # Without delivery fee
    total_no_delivery = order.calculate_total_with_delivery(delivery_option='pickup')
    assert total_no_delivery == 100.0

    # With delivery fee
    total_with_delivery = order.calculate_total_with_delivery(delivery_option='delivery')
    assert total_with_delivery == 110.0  # 100.0 + 10.0 delivery fee
