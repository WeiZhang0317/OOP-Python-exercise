from sqlalchemy.orm import sessionmaker
from db_config import engine
from models.customer import Customer, CorporateCustomer
from models.person import Person
from models.staff import Staff
from models.order import Order, OrderLine, OrderStatus
from models.item import Item, Veggie, WeightedVeggie, PackVeggie, UnitPriceVeggie, PremadeBox
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

# 提交事务，获取生成的 ID
session.commit()

# 获取 customer_id 和 staff_id
customer1 = session.query(Customer).filter_by(username="mikejohnson").first()
customer2 = session.query(Customer).filter_by(username="lucybrown").first()
staff1 = session.query(Staff).filter_by(username="alicewilliams").first()
staff2 = session.query(Staff).filter_by(username="bobtaylor").first()

# 检查并插入 Item 及其子类数据

# 插入 Veggie 数据
if not session.query(Veggie).filter_by(name="Carrot").first():
    veggie1 = Veggie(name="Carrot", price=2.0, veg_name="Carrot")
    session.add(veggie1)
else:
    veggie1 = session.query(Veggie).filter_by(name="Carrot").first()

if not session.query(Veggie).filter_by(name="Spinach").first():
    veggie2 = Veggie(name="Spinach", price=3.0, veg_name="Spinach")
    session.add(veggie2)
else:
    veggie2 = session.query(Veggie).filter_by(name="Spinach").first()

# 插入 WeightedVeggie 数据
if not session.query(WeightedVeggie).filter_by(name="Potato").first():
    weighted_veggie = WeightedVeggie(name="Potato", price=3.0, veg_name="Potato", weight=2.0, weight_per_kilo=1.5)
    session.add(weighted_veggie)
else:
    weighted_veggie = session.query(WeightedVeggie).filter_by(name="Potato").first()

# 插入 PackVeggie 数据
if not session.query(PackVeggie).filter_by(name="Tomato Pack").first():
    pack_veggie = PackVeggie(name="Tomato Pack", price=5.0, veg_name="Tomato", num_of_pack=1, price_per_pack=5.0)
    session.add(pack_veggie)
else:
    pack_veggie = session.query(PackVeggie).filter_by(name="Tomato Pack").first()

# 插入 UnitPriceVeggie 数据
if not session.query(UnitPriceVeggie).filter_by(name="Cucumber").first():
    unit_price_veggie = UnitPriceVeggie(name="Cucumber", price=4.0, veg_name="Cucumber", price_per_unit=0.8, quantity=5)
    session.add(unit_price_veggie)
else:
    unit_price_veggie = session.query(UnitPriceVeggie).filter_by(name="Cucumber").first()

# 插入 PremadeBox 数据
if not session.query(PremadeBox).filter_by(name="Veggie Box").first():
    premade_box = PremadeBox(name="Veggie Box", price=20.0, box_size="Medium", num_of_boxes=1)
    premade_box.add_content([veggie1, veggie2])  # 添加内容
    session.add(premade_box)
else:
    premade_box = session.query(PremadeBox).filter_by(name="Veggie Box").first()

# 提交事务，获取生成的 item_id
session.commit()

# 检查并插入 Order 使用外键 ID
if customer1 and staff1 and not session.query(Order).filter_by(order_number=1001).first():
    order1 = Order(order_number=1001, customer_id=customer1.cust_id, staff_id=staff1.id, order_status=OrderStatus.PENDING.value, total_cost=200.0)
    session.add(order1)

if customer2 and staff2 and not session.query(Order).filter_by(order_number=1002).first():
    order2 = Order(order_number=1002, customer_id=customer2.cust_id, staff_id=staff2.id, order_status=OrderStatus.SHIPPED.value, total_cost=150.0)
    session.add(order2)

# 提交事务，获取生成的 order_id
session.commit()

# 插入 OrderLine 数据
order1 = session.query(Order).filter_by(order_number=1001).first()
order2 = session.query(Order).filter_by(order_number=1002).first()

if order1 and veggie1 and not session.query(OrderLine).filter_by(order_id=order1.id, item_id=veggie1.id).first():
    order_line1 = OrderLine(order_id=order1.id, item_id=veggie1.id, quantity=2, line_total=veggie1.get_price() * 2)
    session.add(order_line1)

if order2 and pack_veggie and not session.query(OrderLine).filter_by(order_id=order2.id, item_id=pack_veggie.id).first():
    order_line2 = OrderLine(order_id=order2.id, item_id=pack_veggie.id, quantity=1, line_total=pack_veggie.get_price())
    session.add(order_line2)

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
