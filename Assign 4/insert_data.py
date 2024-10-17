from sqlalchemy.orm import sessionmaker
from db_config import engine
from models.customer import Customer, CorporateCustomer
from models.person import Person
from models.staff import Staff
from models.order import Order, OrderLine, OrderStatus
from models.item import Veggie, WeightedVeggie, PackVeggie, UnitPriceVeggie, PremadeBox
from models.payment import Payment, CreditCardPayment, DebitCardPayment
from datetime import datetime

# 创建session
Session = sessionmaker(bind=engine)
session = Session()

# 检查并插入Person
if not session.query(Person).filter_by(username="johndoe").first():
    person1 = Person(first_name="John", last_name="Doe", username="johndoe", password="Password123")
    session.add(person1)

if not session.query(Person).filter_by(username="janesmith").first():
    person2 = Person(first_name="Jane", last_name="Smith", username="janesmith", password="Password456")
    session.add(person2)

# 检查并插入Customer
if not session.query(Customer).filter_by(username="mikejohnson").first():
    customer1 = Customer(first_name="Mike", last_name="Johnson", username="mikejohnson", password="Customer123", cust_address="123 Main St", cust_balance=50.0)
    session.add(customer1)

if not session.query(Customer).filter_by(username="lucybrown").first():
    customer2 = Customer(first_name="Lucy", last_name="Brown", username="lucybrown", password="Customer456", cust_address="456 Oak Ave", cust_balance=150.0)
    session.add(customer2)

# 检查并插入CorporateCustomer
if not session.query(CorporateCustomer).filter_by(username="georgewilliams").first():
    corporate_customer1 = CorporateCustomer(first_name="George", last_name="Williams", username="georgewilliams", password="CorpCustomer123", cust_address="789 Pine Rd", cust_balance=600.0, discount_rate=0.15, max_credit=2000.0, min_balance=500.0)
    session.add(corporate_customer1)

if not session.query(CorporateCustomer).filter_by(username="emmagreen").first():
    corporate_customer2 = CorporateCustomer(first_name="Emma", last_name="Green", username="emmagreen", password="CorpCustomer456", cust_address="101 Maple Blvd", cust_balance=800.0, discount_rate=0.12, max_credit=3000.0, min_balance=700.0)
    session.add(corporate_customer2)

# 检查并插入Staff
if not session.query(Staff).filter_by(username="alicewilliams").first():
    staff1 = Staff(first_name="Alice", last_name="Williams", username="alicewilliams", password="Staff123", dept_name="Sales")
    session.add(staff1)

if not session.query(Staff).filter_by(username="bobtaylor").first():
    staff2 = Staff(first_name="Bob", last_name="Taylor", username="bobtaylor", password="Staff456", dept_name="Logistics")
    session.add(staff2)

# 提交事务
session.commit()

# 插入 Payment 数据
if not session.query(Payment).filter_by(payment_amount=45.0, customer_id=customer1.cust_id).first():
    payment1 = Payment(payment_amount=45.0, customer=customer1, payment_date=datetime.now())
    session.add(payment1)

if not session.query(CreditCardPayment).filter_by(card_number="1234567812345678").first():
    credit_payment1 = CreditCardPayment(payment_amount=100.0, customer=customer2, card_number="1234567812345678", card_type="Visa", card_expiry_date="12/25")
    session.add(credit_payment1)

if not session.query(DebitCardPayment).filter_by(debit_card_number="8765432187654321").first():
    debit_payment1 = DebitCardPayment(payment_amount=200.0, customer=corporate_customer1, bank_name="ABC Bank", debit_card_number="8765432187654321")
    session.add(debit_payment1)

# 提交事务
session.commit()

print("数据插入成功！")
