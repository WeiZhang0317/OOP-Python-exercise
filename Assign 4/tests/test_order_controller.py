# python -m pytest -v tests/test_order_controller.py

import pytest
from flask import url_for
from app import app
from models import db
from models.order import Order, OrderStatus
from service.report import SalesReportService, PopularItemReportService

@pytest.fixture
def client():
    """Sets up the test client and database for testing."""
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_current_orders(client):
    """Test displaying all current orders, excluding canceled ones."""
    order1 = Order(order_status=OrderStatus.PENDING.value)
    order2 = Order(order_status=OrderStatus.CANCELED.value)
    db.session.add(order1)
    db.session.add(order2)
    db.session.commit()

    response = client.get(url_for('order.current_orders'))
    assert response.status_code == 200
    assert b'PENDING' in response.data
    assert b'CANCELED' not in response.data  # Ensure canceled orders are excluded

def test_history_orders(client):
    """Test displaying all past orders."""
    order = Order(order_status=OrderStatus.COMPLETED.value)
    db.session.add(order)
    db.session.commit()

    response = client.get(url_for('order.history_orders'))
    assert response.status_code == 200
    assert b'COMPLETED' in response.data  # Check if order status appears in response

def test_detail(client):
    """Test displaying details of a specific order."""
    order = Order(order_status=OrderStatus.SHIPPED.value)
    db.session.add(order)
    db.session.commit()

    response = client.get(url_for('order.detail', order_id=order.id))
    assert response.status_code == 200
    assert b'SHIPPED' in response.data  # Check if order details are displayed

def test_update_status(client):
    """Test updating the status of an order to its next logical status."""
    order = Order(order_status=OrderStatus.PENDING.value)
    db.session.add(order)
    db.session.commit()

    response = client.get(url_for('order.update_status', order_id=order.id))
    assert response.status_code == 302  # Should redirect after update

    updated_order = Order.query.get(order.id)
    assert updated_order.order_status == OrderStatus.SHIPPED.value  # Check if status updated correctly

def test_sales_report(client, mocker):
    """Test generating and displaying the sales report with mocked services."""
    mocker.patch.object(SalesReportService, 'get_weekly_sales', return_value=100)
    mocker.patch.object(SalesReportService, 'get_monthly_sales', return_value=500)
    mocker.patch.object(SalesReportService, 'get_yearly_sales', return_value=2000)
    mocker.patch.object(PopularItemReportService, 'get_popular_items_summary', return_value="Popular Items")
    mocker.patch.object(PopularItemReportService, 'get_least_popular_items_summary', return_value="Least Popular Items")

    response = client.get(url_for('order.sales_report'))
    assert response.status_code == 200
    assert b'100' in response.data       # Weekly sales
    assert b'500' in response.data       # Monthly sales
    assert b'2000' in response.data      # Yearly sales
    assert b'Popular Items' in response.data
    assert b'Least Popular Items' in response.data
