# python -m pytest -v tests/test_payment_model.py

import pytest
from datetime import datetime
from models import db
from models.customer import Customer
from models.payment import Payment, CreditCardPayment, DebitCardPayment
from app import app

@pytest.fixture
def setup_db():
    """Sets up the test client and database for testing."""
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

def test_payment_initialization(setup_db):
    """Test basic initialization of Payment."""
    customer = Customer(first_name="John", last_name="Doe", username="johndoe", password="password", cust_address="123 Main St")
    db.session.add(customer)
    db.session.commit()

    payment = Payment(payment_amount=100.0, customer=customer)
    db.session.add(payment)
    db.session.commit()

    assert payment.payment_amount == 100.0
    assert payment.customer_id == customer.cust_id

def test_credit_card_payment_initialization(setup_db):
    """Test initializing a CreditCardPayment with masked card number."""
    customer = Customer(first_name="Jane", last_name="Doe", username="janedoe", password="password", cust_address="456 Elm St")
    db.session.add(customer)
    db.session.commit()

    payment = CreditCardPayment(
        payment_amount=150.0,
        customer=customer,
        card_number="1234567812345678",
        card_type="Visa",
        card_expiry_date="12/2025"
    )
    db.session.add(payment)
    db.session.commit()

    assert payment.payment_amount == 150.0
    assert payment.card_type == "Visa"
    assert payment.card_number[-4:] == "5678"

    # Check if details return masked card number
    assert "**** **** **** 5678" in payment.get_payment_details()

def test_credit_card_payment_validation(setup_db):
    """Test credit card validation with valid and invalid inputs."""
    # Valid card details
    assert CreditCardPayment.validate_credit_card("1234567812345678", "12/2025", "123") is True

    # Invalid card number
    with pytest.raises(ValueError):
        CreditCardPayment.validate_credit_card("123", "12/2025", "123")

    # Invalid expiry date format
    with pytest.raises(ValueError):
        CreditCardPayment.validate_credit_card("1234567812345678", "2025/12", "123")

    # Invalid CVV
    with pytest.raises(ValueError):
        CreditCardPayment.validate_credit_card("1234567812345678", "12/2025", "12")

def test_credit_card_payment_create(setup_db):
    """Test creating and saving a CreditCardPayment."""
    customer = Customer(first_name="Alice", last_name="Smith", username="alicesmith", password="mypassword", cust_address="789 Oak St")
    db.session.add(customer)
    db.session.commit()

    payment = CreditCardPayment.create_payment(
        customer=customer,
        card_number="9876543210987654",
        card_type="MasterCard",
        expiry_date="11/2024",
        amount=200.0
    )

    assert payment.payment_amount == 200.0
    assert payment.card_type == "MasterCard"
    assert payment.card_number[-4:] == "7654"

def test_debit_card_payment_initialization(setup_db):
    """Test initializing a DebitCardPayment with masked card number."""
    customer = Customer(first_name="Bob", last_name="Johnson", username="bobjohnson", password="password123", cust_address="321 Pine St")
    db.session.add(customer)
    db.session.commit()

    payment = DebitCardPayment(
        payment_amount=120.0,
        customer=customer,
        bank_name="Bank of Python",
        debit_card_number="1111222233334444"
    )
    db.session.add(payment)
    db.session.commit()

    assert payment.payment_amount == 120.0
    assert payment.bank_name == "Bank of Python"
    assert payment.debit_card_number[-4:] == "4444"
    assert "**** **** **** 4444" in payment.get_payment_details()

def test_debit_card_payment_validation(setup_db):
    """Test debit card validation with valid and invalid inputs."""
    # Valid debit card number
    assert DebitCardPayment.validate_debit_card("1111222233334444") is True

    # Invalid debit card number
    with pytest.raises(ValueError):
        DebitCardPayment.validate_debit_card("1234")

def test_debit_card_payment_create(setup_db):
    """Test creating and saving a DebitCardPayment."""
    customer = Customer(first_name="Eve", last_name="Black", username="eveblack", password="strongpass", cust_address="456 Maple St")
    db.session.add(customer)
    db.session.commit()

    payment = DebitCardPayment.create_payment(
        customer=customer,
        bank_name="Python Bank",
        card_number="2222333344445555",
        amount=75.0
    )

    assert payment.payment_amount == 75.0
    assert payment.bank_name == "Python Bank"
    assert payment.debit_card_number[-4:] == "5555"
