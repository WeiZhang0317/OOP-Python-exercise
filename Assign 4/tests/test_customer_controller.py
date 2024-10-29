import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from flask import url_for, session
from app import app  # Assuming your Flask app instance is in app.py
from models import db, Customer, CorporateCustomer, Order
from service.report import SalesReportService
# python -m pytest -v tests/test_customer_controller.py
# Using pytest fixture to create a test client
@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            # Initialize test database (if needed)
            db.create_all()
            # Add test data
            customer = Customer(name="Test Customer", balance=100)
            corporate_customer = CorporateCustomer(name="Test Corporate Customer", balance=500)
            order = Order(customer_id=1, amount=50)
            db.session.add(customer)
            db.session.add(corporate_customer)
            db.session.add(order)
            db.session.commit()
        yield client
        # Clean up the database after testing
        db.session.remove()
        db.drop_all()

# Test customer_list route
def test_customer_list(client):
    response = client.get(url_for('customer.customer_list'))
    assert response.status_code == 200
    assert b'Test Customer' in response.data  # Check for content on the page

# Test customer_detail route
def test_customer_detail(client, mocker):
    # Mock SalesReportService methods
    mocker.patch.object(SalesReportService, 'get_weekly_sales', return_value=100)
    mocker.patch.object(SalesReportService, 'get_monthly_sales', return_value=500)
    mocker.patch.object(SalesReportService, 'get_yearly_sales', return_value=1000)

    response = client.get(url_for('customer.customer_detail', customer_id=1))
    assert response.status_code == 200
    assert b'Test Customer' in response.data  # Check for content on the page

# Test corporate_customer_list route
def test_corporate_customer_list(client):
    response = client.get(url_for('customer.corporate_customer_list'))
    assert response.status_code == 200
    assert b'Test Corporate Customer' in response.data  # Check for content on the page

# Test corporate_customer_detail route
def test_corporate_customer_detail(client, mocker):
    mocker.patch.object(SalesReportService, 'get_weekly_sales', return_value=200)
    mocker.patch.object(SalesReportService, 'get_monthly_sales', return_value=800)
    mocker.patch.object(SalesReportService, 'get_yearly_sales', return_value=1500)

    response = client.get(url_for('customer.corporate_customer_detail', customer_id=1))
    assert response.status_code == 200
    assert b'Test Corporate Customer' in response.data  # Check for content on the page

# Test history_orders route
def test_history_orders(client):
    with client.session_transaction() as sess:
        sess['user_id'] = 1  # Simulate logged-in user

    response = client.get(url_for('customer.history_orders'))
    assert response.status_code == 200
    assert b'Order History' in response.data  # Assuming the page shows order history

# Test detail route
def test_order_detail(client):
    with client.session_transaction() as sess:
        sess['user_id'] = 1  # Simulate logged-in user

    response = client.get(url_for('customer.detail', order_id=1))
    assert response.status_code == 200
    assert b'Order Details' in response.data  # Assuming the page shows order details

# Test customer_profile route
def test_customer_profile(client):
    with client.session_transaction() as sess:
        sess['user_id'] = 1  # Simulate logged-in user

    response = client.get(url_for('customer.customer_profile'))
    assert response.status_code == 200
    assert b'Test Customer' in response.data  # Check for content on the page
