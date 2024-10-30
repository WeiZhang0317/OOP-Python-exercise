# python -m pytest -v tests/test_controllers_service/test_report_service.py

import pytest
from datetime import datetime, timedelta
from models import db
from models.order import Order, OrderStatus, OrderLine
from models.item import Item
from service.report import SalesReportService, PopularItemReportService
from app import app

@pytest.fixture
def setup_db():
    """Sets up the test client and database for testing."""
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

def create_order(customer_id, total_cost, order_status, days_ago=0):
    """Helper function to create an order with a given date offset by days."""
    order_date = datetime.now() - timedelta(days=days_ago)
    order = Order(
        order_number=Order.generate_unique_order_number(),
        customer_id=customer_id,
        staff_id=1,
        order_status=order_status,
        total_cost=total_cost
    )
    db.session.add(order)
    db.session.commit()
    return order

def test_get_sales_total(setup_db):
    """Test calculating total sales for the last 7 days."""
    create_order(customer_id=1, total_cost=100.0, order_status=OrderStatus.PAID.value, days_ago=2)
    create_order(customer_id=1, total_cost=50.0, order_status=OrderStatus.SHIPPED.value, days_ago=5)
    create_order(customer_id=2, total_cost=30.0, order_status=OrderStatus.CANCELED.value, days_ago=6)

    total_sales = SalesReportService.get_sales_total(7)
    assert total_sales == 150.0  # Excludes canceled order

def test_get_weekly_sales(setup_db):
    """Test weekly sales calculation."""
    create_order(customer_id=1, total_cost=80.0, order_status=OrderStatus.PAID.value, days_ago=3)
    create_order(customer_id=2, total_cost=20.0, order_status=OrderStatus.PAID.value, days_ago=6)
    
    weekly_sales = SalesReportService.get_weekly_sales()
    assert weekly_sales == 100.0

def test_get_monthly_sales(setup_db):
    """Test monthly sales calculation."""
    create_order(customer_id=1, total_cost=120.0, order_status=OrderStatus.PAID.value, days_ago=15)
    create_order(customer_id=2, total_cost=180.0, order_status=OrderStatus.SHIPPED.value, days_ago=25)
    
    monthly_sales = SalesReportService.get_monthly_sales()
    assert monthly_sales == 300.0

def test_get_yearly_sales(setup_db):
    """Test yearly sales calculation."""
    create_order(customer_id=1, total_cost=250.0, order_status=OrderStatus.PAID.value, days_ago=100)
    create_order(customer_id=2, total_cost=450.0, order_status=OrderStatus.SHIPPED.value, days_ago=200)
    
    yearly_sales = SalesReportService.get_yearly_sales()
    assert yearly_sales == 700.0

def create_order_with_item(item_name, quantity, line_total):
    """Helper function to create an order and attach an item as an OrderLine."""
    item = Item(name=item_name, price=line_total / quantity)
    db.session.add(item)
    db.session.commit()

    order = create_order(customer_id=1, total_cost=line_total, order_status=OrderStatus.PAID.value)
    order_line = OrderLine(order_id=order.id, item_id=item.id, quantity=quantity, line_total=line_total)
    db.session.add(order_line)
    db.session.commit()
    return item

def test_get_most_sold_item(setup_db):
    """Test retrieving the most sold item by quantity."""
    create_order_with_item("Apple", 10, 20.0)
    create_order_with_item("Banana", 15, 30.0)

    most_sold = PopularItemReportService.get_most_sold_item()
    assert most_sold["item_name"] == "Banana"
    assert most_sold["total"] == 15

def test_get_highest_revenue_item(setup_db):
    """Test retrieving the item with the highest total revenue."""
    create_order_with_item("Orange", 5, 50.0)
    create_order_with_item("Grapes", 3, 75.0)

    highest_revenue = PopularItemReportService.get_highest_revenue_item()
    assert highest_revenue["item_name"] == "Grapes"
    assert highest_revenue["total"] == 75.0

def test_get_most_frequent_item(setup_db):
    """Test retrieving the most frequent item in orders."""
    create_order_with_item("Watermelon", 2, 10.0)
    create_order_with_item("Watermelon", 3, 15.0)  # Adding same item in different orders

    most_frequent = PopularItemReportService.get_most_frequent_item()
    assert most_frequent["item_name"] == "Watermelon"
    assert most_frequent["total"] == 2  # Appears in 2 orders

def test_get_least_sold_item(setup_db):
    """Test retrieving the least sold item by quantity."""
    create_order_with_item("Pineapple", 8, 40.0)
    create_order_with_item("Peach", 5, 25.0)

    least_sold = PopularItemReportService.get_least_sold_item()
    assert least_sold["item_name"] == "Peach"
    assert least_sold["total"] == 5

def test_get_lower_revenue_item(setup_db):
    """Test retrieving the item with the lowest revenue."""
    create_order_with_item("Mango", 3, 30.0)
    create_order_with_item("Cherry", 4, 20.0)

    lower_revenue = PopularItemReportService.get_lower_revenue_item()
    assert lower_revenue["item_name"] == "Cherry"
    assert lower_revenue["total"] == 20.0

def test_get_least_frequent_item(setup_db):
    """Test retrieving the least frequent item in orders."""
    create_order_with_item("Kiwi", 2, 8.0)
    create_order_with_item("Strawberry", 1, 5.0)  # Only appears in one order

    least_frequent = PopularItemReportService.get_least_frequent_item()
    assert least_frequent["item_name"] == "Strawberry"
    assert least_frequent["total"] == 1  # Appears in 1 order
