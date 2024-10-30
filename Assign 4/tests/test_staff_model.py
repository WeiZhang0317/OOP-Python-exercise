import pytest
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from models import Staff, Customer, PremadeBox, Veggie, db
from werkzeug.security import generate_password_hash

@pytest.fixture
def create_staff():
    """Create a sample staff member for testing."""
    return Staff(
        first_name="John",
        last_name="Doe",
        username="johndoe",
        password=generate_password_hash("password123"),
        dept_name="Sales"
    )

def test_staff_creation(db_session, create_staff):
    """Test creating a Staff member with correct fields."""
    staff = create_staff
    db.session.add(staff)
    db.session.commit()

    # Check if the staff member is successfully added
    assert staff.id is not None
    assert staff.first_name == "John"
    assert staff.last_name == "Doe"
    assert staff.username == "johndoe"
    assert staff.dept_name == "Sales"
    assert staff.date_joined.date() == datetime.now().date()

def test_staff_relationships(db_session, create_staff):
    """Test Staff relationships with Orders, Customers, PremadeBox, and Veggie."""
    staff = create_staff

    # Add relationships data for testing
    customer = Customer(first_name="Alice", last_name="Wonder", username="alicewonder", password="pass123")
    premade_box = PremadeBox(name="Veggie Box", price=20.0, box_size="medium")
    veggie = Veggie(name="Carrot", price=1.5, veg_name="Carrot")

    # Add objects to the session
    db.session.add_all([staff, customer, premade_box, veggie])
    db.session.commit()

    # Append objects to staff lists
    staff.list_of_customers.append(customer)
    staff.premade_boxes.append(premade_box)
    staff.veggie.append(veggie)
    db.session.commit()

    # Validate relationships
    assert len(staff.list_of_customers) == 1
    assert len(staff.premade_boxes) == 1
    assert len(staff.veggie) == 1

def test_staff_str_method(create_staff):
    """Test the __str__ method of the Staff class."""
    staff = create_staff
    expected_str = (f"Staff ID: {staff.id}, Name: {staff.get_full_name()}, "
                    f"Department: {staff.dept_name}, Date Joined: {staff.date_joined.strftime('%Y-%m-%d')}, "
                    f"Number of Managed Customers: {len(staff.list_of_customers)}, "
                    f"Number of Managed Orders: {len(staff.list_of_orders)}")
    
    assert str(staff) == expected_str
