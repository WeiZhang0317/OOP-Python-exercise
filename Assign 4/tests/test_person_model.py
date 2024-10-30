#python -m pytest -v tests/test_person_model.py

import pytest
from werkzeug.security import generate_password_hash
from models import db
from models.person import Person  # Import the Person class from your models
from app import app  # Assuming your Flask app instance is in app.py

@pytest.fixture
def setup_db():
    """Sets up the test client and database for testing."""
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

def test_person_initialization(setup_db):
    """Test initializing a Person instance."""
    password_hash = generate_password_hash("password123")
    person = Person(
        first_name="John",
        last_name="Doe",
        username="johndoe",
        password=password_hash,
        role="user"
    )
    db.session.add(person)
    db.session.commit()
    
    assert person.first_name == "John"
    assert person.last_name == "Doe"
    assert person.username == "johndoe"
    assert person.role == "user"
    assert person._Person__password == password_hash  # Check if password is correctly set

def test_get_full_name(setup_db):
    """Test the get_full_name method."""
    person = Person(
        first_name="Jane",
        last_name="Smith",
        username="janesmith",
        password=generate_password_hash("securepass"),
        role="admin"
    )
    assert person.get_full_name() == "Jane Smith"

def test_check_password(setup_db):
    """Test the check_password method for password verification."""
    password = "mypassword"
    person = Person(
        first_name="Alice",
        last_name="Wonder",
        username="alicew",
        password=generate_password_hash(password),
        role="editor"
    )
    db.session.add(person)
    db.session.commit()
    
    assert person.check_password(password) is True  # Correct password
    assert person.check_password("wrongpassword") is False  # Incorrect password

def test_person_str_method(setup_db):
    """Test the __str__ method for proper string representation."""
    person = Person(
        first_name="Bob",
        last_name="Marley",
        username="bobmarley",
        password=generate_password_hash("reggaepass"),
        role="musician"
    )
    expected_str = "Name: Bob Marley, Username: bobmarley, Role: musician"
    assert str(person) == expected_str
