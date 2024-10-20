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


# 检查并插入 Item 及其子类数据

# 插入 Veggie 数据
if not session.query(Veggie).filter_by(name="Carrot").first():
    veggie1 = Veggie(name="Carrot", price=2.0, veg_name="Carrot")
    session.add(veggie1)

if not session.query(Veggie).filter_by(name="Spinach").first():
    veggie2 = Veggie(name="Spinach", price=3.0, veg_name="Spinach")
    session.add(veggie2)

if not session.query(Veggie).filter_by(name="Broccoli").first():
    veggie3 = Veggie(name="Broccoli", price=4.0, veg_name="Broccoli")
    session.add(veggie3)

if not session.query(Veggie).filter_by(name="Lettuce").first():
    veggie4 = Veggie(name="Lettuce", price=3.5, veg_name="Lettuce")
    session.add(veggie4)

# 插入 WeightedVeggie 数据
if not session.query(WeightedVeggie).filter_by(name="Potato").first():
    weighted_veggie = WeightedVeggie(name="Potato", price=1.5, veg_name="Potato", weight=2.0, weight_per_kilo=1.5)
    session.add(weighted_veggie)

if not session.query(WeightedVeggie).filter_by(name="Sweet Potato").first():
    weighted_veggie2 = WeightedVeggie(name="Sweet Potato", price=5.0, veg_name="Sweet Potato", weight=2.5, weight_per_kilo=2.0)
    session.add(weighted_veggie2)

# 插入 PackVeggie 数据
if not session.query(PackVeggie).filter_by(name="Tomato Pack").first():
    pack_veggie = PackVeggie(name="Tomato Pack", price=5.0, veg_name="Tomato", num_of_pack=1, price_per_pack=5.0)
    session.add(pack_veggie)

if not session.query(PackVeggie).filter_by(name="Pepper Pack").first():
    pack_veggie2 = PackVeggie(name="Pepper Pack", price=8.0, veg_name="Pepper", num_of_pack=2, price_per_pack=4.0)
    session.add(pack_veggie2)

# 插入 UnitPriceVeggie 数据
if not session.query(UnitPriceVeggie).filter_by(name="Cucumber").first():
    unit_price_veggie = UnitPriceVeggie(name="Cucumber", price=0.8, veg_name="Cucumber", price_per_unit=0.8, quantity=5)
    session.add(unit_price_veggie)

if not session.query(UnitPriceVeggie).filter_by(name="Eggplant").first():
    unit_price_veggie2 = UnitPriceVeggie(name="Eggplant", price=3.0, veg_name="Eggplant", price_per_unit=1.5, quantity=2)
    session.add(unit_price_veggie2)

# 插入 PremadeBox 数据
if not session.query(PremadeBox).filter_by(name="Veggie Box").first():
    premade_box = PremadeBox(name="Veggie Box", price=20.0, box_size="Medium", num_of_boxes=1)
    premade_box.add_content([veggie1, veggie2])
    session.add(premade_box)

if not session.query(PremadeBox).filter_by(name="Large Veggie Box").first():
    premade_box2 = PremadeBox(name="Large Veggie Box", price=30.0, box_size="Large", num_of_boxes=2)
    premade_box2.add_content([veggie3, veggie4])
    session.add(premade_box2)

# 提交事务
session.commit()

# 检查并插入 Order 使用外键 ID
if customer1 and staff1 and not session.query(Order).filter_by(order_number=1001).first():
    order1 = Order(order_number=1001, customer_id=customer1.cust_id, staff_id=staff1.id, order_status=OrderStatus.PENDING.value, total_cost=200.0)
    session.add(order1)

if customer2 and staff2 and not session.query(Order).filter_by(order_number=1002).first():
    order2 = Order(order_number=1002, customer_id=customer2.cust_id, staff_id=staff2.id, order_status=OrderStatus.SHIPPED.value, total_cost=150.0)
    session.add(order2)

if customer3 and staff3 and not session.query(Order).filter_by(order_number=1003).first():
    order3 = Order(order_number=1003, customer_id=customer3.cust_id, staff_id=staff3.id, order_status=OrderStatus.PENDING.value, total_cost=100.0)
    session.add(order3)

if customer4 and staff4 and not session.query(Order).filter_by(order_number=1004).first():
    order4 = Order(order_number=1004, customer_id=customer4.cust_id, staff_id=staff4.id, order_status=OrderStatus.SHIPPED.value, total_cost=200.0)
    session.add(order4)

# 提交事务
session.commit()

# 插入 OrderLine 数据
order1 = session.query(Order).filter_by(order_number=1001).first()
order2 = session.query(Order).filter_by(order_number=1002).first()
order3 = session.query(Order).filter_by(order_number=1003).first()
order4 = session.query(Order).filter_by(order_number=1004).first()

if order1 and veggie1 and not session.query(OrderLine).filter_by(order_id=order1.id, item_id=veggie1.id).first():
    order_line1 = OrderLine(order_id=order1.id, item_id=veggie1.id, quantity=2, line_total=veggie1.get_price() * 2)
    session.add(order_line1)

if order2 and pack_veggie and not session.query(OrderLine).filter_by(order_id=order2.id, item_id=pack_veggie.id).first():
    order_line2 = OrderLine(order_id=order2.id, item_id=pack_veggie.id, quantity=1, line_total=pack_veggie.get_price())
    session.add(order_line2)

if order3 and veggie3 and not session.query(OrderLine).filter_by(order_id=order3.id, item_id=veggie3.id).first():
    order_line3 = OrderLine(order_id=order3.id, item_id=veggie3.id, quantity=3, line_total=veggie3.get_price() * 3)
    session.add(order_line3)

if order4 and premade_box2 and not session.query(OrderLine).filter_by(order_id=order4.id, item_id=premade_box2.id).first():
    order_line4 = OrderLine(order_id=order4.id, item_id=premade_box2.id, quantity=1, line_total=premade_box2.get_price())
    session.add(order_line4)

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

if not session.query(Payment).filter_by(payment_amount=75.0, customer_id=customer3.cust_id).first():
    payment2 = Payment(payment_amount=75.0, customer=customer3, payment_date=datetime.now())
    session.add(payment2)

if not session.query(CreditCardPayment).filter_by(card_number="9876543212345678").first():
    credit_payment2 = CreditCardPayment(payment_amount=150.0, customer=customer4, card_number="9876543212345678", card_type="MasterCard", card_expiry_date="11/26")
    session.add(credit_payment2)

if not session.query(DebitCardPayment).filter_by(debit_card_number="1234567812348765").first():
    debit_payment2 = DebitCardPayment(payment_amount=250.0, customer=corporate_customer3, bank_name="XYZ Bank", debit_card_number="1234567812348765")
    session.add(debit_payment2)

# 提交事务
session.commit()

print("数据插入成功！")
