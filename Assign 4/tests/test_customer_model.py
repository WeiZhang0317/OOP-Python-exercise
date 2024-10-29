import pytest
from models import db
from models.customer import Customer
from app import app

# python -m pytest -v tests/test_customer_model.py

@pytest.fixture
def setup_db():
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

def test_customer_initialization(setup_db):
    """Test initializing a Customer instance."""
    customer = Customer(
        first_name="John",
        last_name="Doe",
        username="johndoe",
        password="password123",
        cust_address="123 Main St",
        cust_balance=50.0
    )
    db.session.add(customer)
    db.session.commit()
    
    assert customer.first_name == "John"
    assert customer.last_name == "Doe"
    assert customer.cust_address == "123 Main St"
    assert customer.cust_balance == 50.0
    assert customer.max_owing == 100.0

def test_can_place_order_based_on_balance(setup_db):
    """Test `can_place_order_based_on_balance` method based on balance."""
    customer = Customer(
        first_name="Jane",
        last_name="Smith",
        username="janesmith",
        password="securepass",
        cust_address="456 Elm St",
        cust_balance=-80.0
    )
    db.session.add(customer)
    db.session.commit()
    
    # Customer should be able to place an order if the balance is within max owing
    assert customer.can_place_order_based_on_balance() is True

    # Set balance below allowable limit
    customer.cust_balance = -120.0
    db.session.commit()
    
    # Customer should not be able to place an order with a balance below the max owing
    assert customer.can_place_order_based_on_balance() is False

def test_deduct_balance(setup_db):
    """Test `deduct_balance` method for various scenarios."""
    customer = Customer(
        first_name="Alice",
        last_name="Wonder",
        username="alicew",
        password="mypassword",
        cust_address="789 Oak St",
        cust_balance=30.0
    )
    db.session.add(customer)
    db.session.commit()
    
    # Successful deduction within the limit
    assert customer.deduct_balance(20.0) is True
    assert customer.cust_balance == 10.0

    # Deduction exceeding max owing limit
    customer.cust_balance = -90.0
    db.session.commit()
    assert customer.deduct_balance(20.0) is False
    assert customer.cust_balance == -90.0

def test_make_payment(setup_db):
    """Test `make_payment` method by adding a mock payment."""
    customer = Customer(
        first_name="Eve",
        last_name="Adams",
        username="eveadams",
        password="password456",
        cust_address="321 Pine St",
        cust_balance=-50.0
    )
    db.session.add(customer)
    db.session.commit()
    
    # Create a mock payment object
    class MockPayment:
        payment_amount = 20.0
    
    # Attempt payment
    customer.make_payment(MockPayment())
    
    # Verify payment has been applied
    assert customer.cust_balance == -70.0
    assert len(customer.list_of_payments) == 1

def test_view_order_history(setup_db, capsys):
    """Test `view_order_history` method output."""
    customer = Customer(
        first_name="Bob",
        last_name="Marley",
        username="bobmarley",
        password="jammin123",
        cust_address="No Woman St"
    )
    db.session.add(customer)
    db.session.commit()
    
    # Capture output when viewing order history with no orders
    customer.view_order_history()
    captured = capsys.readouterr()
    assert "No orders found in your history." in captured.out
