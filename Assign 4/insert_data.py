from sqlalchemy.orm import sessionmaker
from db_config import engine
from models.customer import Customer, CorporateCustomer
from models.person import Person
from models.staff import Staff
from models.order import Order, OrderLine, OrderStatus
from models.item import Veggie, WeightedVeggie, PackVeggie, UnitPriceVeggie, PremadeBox
from models.payment import Payment, CreditCardPayment, DebitCardPayment
from datetime import datetime

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

#  Person 
person1 = Person(first_name="John", last_name="Doe", username="johndoe", password="Password123")
person2 = Person(first_name="Jane", last_name="Smith", username="janesmith", password="Password456")

#Customer 
customer1 = Customer(first_name="Mike", last_name="Johnson", username="mikejohnson", password="Customer123", cust_address="123 Main St", cust_balance=50.0)
customer2 = Customer(first_name="Lucy", last_name="Brown", username="lucybrown", password="Customer456", cust_address="456 Oak Ave", cust_balance=150.0)

# CorporateCustomer
corporate_customer1 = CorporateCustomer(first_name="George", last_name="Williams", username="georgewilliams", password="CorpCustomer123", cust_address="789 Pine Rd", cust_balance=600.0, discount_rate=0.15, max_credit=2000.0, min_balance=500.0)
corporate_customer2 = CorporateCustomer(first_name="Emma", last_name="Green", username="emmagreen", password="CorpCustomer456", cust_address="101 Maple Blvd", cust_balance=800.0, discount_rate=0.12, max_credit=3000.0, min_balance=700.0)

# Staff 
staff1 = Staff(first_name="Alice", last_name="Williams", username="alicewilliams", password="Staff123", dept_name="Sales")
staff2 = Staff(first_name="Bob", last_name="Taylor", username="bobtaylor", password="Staff456", dept_name="Logistics")

session.add(person1)
session.add(person2)
session.add(customer1)
session.add(customer2)
session.add(corporate_customer1)
session.add(corporate_customer2)
session.add(staff1)
session.add(staff2)


session.commit()

# # Insert Items
# item1 = Veggie(name="Carrot", price=2.00, veg_name="Carrot")
# item2 = WeightedVeggie(name="Potato", price=3.00, veg_name="Potato", weight=1.5, weight_per_kilo=2.50)
# item3 = PackVeggie(name="Spinach Pack", price=5.00, veg_name="Spinach", num_of_pack=1, price_per_pack=5.00)
# item4 = UnitPriceVeggie(name="Tomato", price=1.00, veg_name="Tomato", price_per_unit=1.00, quantity=5)
# premade_box = PremadeBox(name="Medium Veggie Box", price=25.00, box_size="Medium", num_of_boxes=1)

# # Insert Orders
# order1 = Order(order_number=101, order_customer=customer1, list_of_order_lines=[], order_status=OrderStatus.PENDING.value)
# order2 = Order(order_number=102, order_customer=customer2, list_of_order_lines=[], order_status=OrderStatus.PAID.value)

# # Insert OrderLines
# order_line1 = OrderLine(item=item1, quantity=10)
# order_line2 = OrderLine(item=item2, quantity=2)
# order_line3 = OrderLine(item=premade_box, quantity=1)

# order1.add_order_line(order_line1)
# order1.add_order_line(order_line2)
# order2.add_order_line(order_line3)

# # Insert Payments
# payment1 = CreditCardPayment(payment_amount=50.00, card_number="1234567812345678", card_type="Visa", card_expiry_date="2024-10")
# payment2 = DebitCardPayment(payment_amount=100.00, bank_name="ABC Bank", debit_card_number="8765432187654321")

# # Commit all inserts to the database
# session.add_all([customer1, customer2, staff1, item1, item2, item3, item4, premade_box, order1, order2, order_line1, order_line2, order_line3, payment1, payment2])
# session.commit()

print("Data inserted successfully!")
