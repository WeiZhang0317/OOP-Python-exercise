import sys
import os
import random
# pytest --cov=./ --cov-report=term-missing --cov-report=html -v tests/

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app import app as flask_app
from models import db, Customer, CorporateCustomer, Person, Staff, Item, Inventory, PremadeBox, Veggie, WeightedVeggie, PackVeggie, UnitPriceVeggie
from werkzeug.security import generate_password_hash

# 设置测试数据库
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(TEST_DATABASE_URL)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))  # 使用 scoped_session 管理

print("Loading conftest.py")  # 用于调试，确保加载此文件


@pytest.fixture(scope="session")
def app():
    """Create a test Flask application."""
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DATABASE_URL
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with flask_app.app_context():
        db.init_app(flask_app)
        db.create_all()  # Create tables
        yield flask_app
        db.drop_all()  # Drop tables after tests

@pytest.fixture(scope="function")
def db_session(app):
    """Set up a database session for each test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)
    db.session = session

    # Insert initial test data
    insert_test_data(session)

    yield session

    session.close()
    transaction.rollback()
    connection.close()
    SessionLocal.remove()  # Ensure scoped_session cleanup

@pytest.fixture(scope="function")
def client(app, db_session):
    """Provide a Flask test client."""
    with app.test_client() as client:
        yield client

def insert_test_data(session):
    """Insert initial data with hashed passwords and item setup."""
    # Inserting customers and staff
    customer1 = Customer(
        first_name="Alice",
        last_name="Wonder",
        username="alice_wonder",
        password=generate_password_hash("CustomerPass123"),
        cust_balance=100,
        cust_address="123 Fantasy Road, Wonderland"
    )
    customer2 = Customer(
        first_name="Bob",
        last_name="Builder",
        username="bob_builder",
        password=generate_password_hash("CustomerPass123"),
        cust_balance=-100,
        cust_address="456 Construction Ave, Buildtown"
    )
    corporate_customer = CorporateCustomer(
        first_name="Karen",
        last_name="Corporate",
        username="corporate_karen",
        password=generate_password_hash("CorporatePass456"),
        cust_balance=200,
        discount_rate=0.10,
        max_credit=2000.0,
        min_balance=1000.0,
        cust_address="789 Business Blvd, Corporatia"
    )
    staff = Staff(
        first_name="John",
        last_name="Staffer",
        username="staff_john",
        password=generate_password_hash("StaffPass789"),
        dept_name="Sales"
    )
    session.add_all([customer1, customer2, corporate_customer, staff])

    # Inserting various veggies and premade boxes
    veggies = [("Capsicum", 2.0), ("Cucumber", 1.5), ("Broccoli", 4.0), ("Lettuce", 3.5)]
    for name, price in veggies:
        veggie = Veggie(name=name, price=price, veg_name=name)
        session.add(veggie)

    weighted_veggies = [("Potato", 1.5, "kg"), ("Sweet Potato", 2.0, "kg")]
    for name, price, unit in weighted_veggies:
        weighted_veggie = WeightedVeggie(name=name, price=price, veg_name=name, weight_per_kilo=price, unit_type=unit)
        session.add(weighted_veggie)

    pack_veggies = [("Tomato Pack", 5.0, 3), ("Mushroom Pack", 6.0, 7)]
    for name, price, num in pack_veggies:
        pack_veggie = PackVeggie(name=name, price=price, veg_name=name.split()[0], num_in_pack=num)
        session.add(pack_veggie)

    unit_price_veggies = [("Bok choy", 5.5, "bunch"), ("Spring onion", 3.0, "bunch")]
    for name, price, unit in unit_price_veggies:
        unit_price_veggie = UnitPriceVeggie(name=name, price=price, veg_name=name, price_per_unit=price, unit_type=unit)
        session.add(unit_price_veggie)

    premade_boxes = [
        ("Small Veggie Box", 15.0, "small"),
        ("Medium Veggie Box", 20.0, "medium"),
        ("Large Veggie Box", 30.0, "large")
    ]
    for name, price, size in premade_boxes:
        premade_box = PremadeBox(name=name, price=price, box_size=size)
        session.add(premade_box)

    session.commit()

    # Adding inventory for all items
    items = session.query(Item).all()
    for item in items:
        inventory_entry = Inventory(item_id=item.id, quantity=random.randint(80, 200))
        session.add(inventory_entry)

    session.commit()