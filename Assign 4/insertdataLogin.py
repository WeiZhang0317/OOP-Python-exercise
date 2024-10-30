from sqlalchemy.orm import sessionmaker
from db_config import engine
from models.customer import Customer, CorporateCustomer
from models.person import Person
from models.staff import Staff
from werkzeug.security import generate_password_hash
from datetime import datetime


Session = sessionmaker(bind=engine)
session = Session()


if not session.query(Person).filter_by(username="alice_wonder").first():
    customer1 = Customer(
        first_name="Alice",
        last_name="Wonder",
        username="alice_wonder",
        password="CustomerPass123",  
        cust_balance=100,
        cust_address="123 Fantasy Road, Wonderland"
    )
    session.add(customer1)


if not session.query(Person).filter_by(username="bob_builder").first():
    customer2 = Customer(
        first_name="Bob",
        last_name="Builder",
        username="bob_builder",
        password="CustomerPass123",  
        cust_balance=-100,
        cust_address="456 Construction Ave, Buildtown"
    )
    session.add(customer2)


if not session.query(Person).filter_by(username="corporate_karen").first():
    corporate_customer = CorporateCustomer(
        first_name="Karen",
        last_name="Corporate",
        username="corporate_karen",
        password="CorporatePass456", 
        cust_address="789 Business Blvd, Corporatia",
        cust_balance=200,
        discount_rate=0.10,  
        max_credit=2000.0,   
        min_balance=1000.0   
    )
    session.add(corporate_customer)
    

if not session.query(Person).filter_by(username="corporate_Liz").first():
    corporate_customer = CorporateCustomer(
        first_name="Liz",
        last_name="Corporate",
        username="corporate_Liz",
        password="CorporatePass456",  
        cust_address="789 Fair Road, Corporatia",
        cust_balance=15000,
        discount_rate=0.10,  
        max_credit=2000.0,   
        min_balance=1000.0   
    )
    session.add(corporate_customer)    


if not session.query(Person).filter_by(username="staff_john").first():
    staff = Staff(
        first_name="John",
        last_name="Staffer",
        username="staff_john",
        password="StaffPass789", 
        dept_name="Sales"
    )
    session.add(staff)


session.commit()


persons = session.query(Person).all()
for person in persons:
    #  (Werkzeug hashes start with 'pbkdf2:sha256')
    if not person._Person__password.startswith('pbkdf2:sha256'):
        # Encrypt the plain-text password
        hashed_password = generate_password_hash(person._Person__password)
        person._Person__password = hashed_password


session.commit()

print("Data inserted and passwords encrypted successfully!")


session.close()
