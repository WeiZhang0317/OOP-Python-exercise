from sqlalchemy.orm import sessionmaker
from db_config import engine
from models.customer import Customer, CorporateCustomer
from models.person import Person
from models.staff import Staff
from models.order import Order, OrderLine, OrderStatus
from models.item import Item, Veggie, WeightedVeggie, PackVeggie, UnitPriceVeggie, PremadeBox, Inventory  # 从 models.item 中导入 Inventory
from models.payment import Payment, CreditCardPayment, DebitCardPayment
from datetime import datetime

# 创建session
Session = sessionmaker(bind=engine)
session = Session()

# 插入 Inventory 数据
# 获取已经插入的蔬菜和盒子对象
veggie1 = session.query(Veggie).filter_by(name="Carrot").first()
veggie2 = session.query(Veggie).filter_by(name="Spinach").first()
veggie3 = session.query(Veggie).filter_by(name="Broccoli").first()
veggie4 = session.query(Veggie).filter_by(name="Lettuce").first()
weighted_veggie = session.query(WeightedVeggie).filter_by(name="Potato").first()
weighted_veggie2 = session.query(WeightedVeggie).filter_by(name="Sweet Potato").first()
pack_veggie = session.query(PackVeggie).filter_by(name="Tomato Pack").first()
pack_veggie2 = session.query(PackVeggie).filter_by(name="Pepper Pack").first()
unit_price_veggie = session.query(UnitPriceVeggie).filter_by(name="Cucumber").first()
unit_price_veggie2 = session.query(UnitPriceVeggie).filter_by(name="Eggplant").first()
premade_box = session.query(PremadeBox).filter_by(name="Veggie Box").first()
premade_box2 = session.query(PremadeBox).filter_by(name="Large Veggie Box").first()

# 为每个商品插入库存数据
if veggie1 and not session.query(Inventory).filter_by(item_id=veggie1.id).first():
    inventory_veggie1 = Inventory(item_id=veggie1.id, quantity=50)
    session.add(inventory_veggie1)

if veggie2 and not session.query(Inventory).filter_by(item_id=veggie2.id).first():
    inventory_veggie2 = Inventory(item_id=veggie2.id, quantity=30)
    session.add(inventory_veggie2)

if veggie3 and not session.query(Inventory).filter_by(item_id=veggie3.id).first():
    inventory_veggie3 = Inventory(item_id=veggie3.id, quantity=40)
    session.add(inventory_veggie3)

if veggie4 and not session.query(Inventory).filter_by(item_id=veggie4.id).first():
    inventory_veggie4 = Inventory(item_id=veggie4.id, quantity=20)
    session.add(inventory_veggie4)

if weighted_veggie and not session.query(Inventory).filter_by(item_id=weighted_veggie.id).first():
    inventory_weighted_veggie = Inventory(item_id=weighted_veggie.id, quantity=60)
    session.add(inventory_weighted_veggie)

if weighted_veggie2 and not session.query(Inventory).filter_by(item_id=weighted_veggie2.id).first():
    inventory_weighted_veggie2 = Inventory(item_id=weighted_veggie2.id, quantity=35)
    session.add(inventory_weighted_veggie2)

if pack_veggie and not session.query(Inventory).filter_by(item_id=pack_veggie.id).first():
    inventory_pack_veggie = Inventory(item_id=pack_veggie.id, quantity=25)
    session.add(inventory_pack_veggie)

if pack_veggie2 and not session.query(Inventory).filter_by(item_id=pack_veggie2.id).first():
    inventory_pack_veggie2 = Inventory(item_id=pack_veggie2.id, quantity=15)
    session.add(inventory_pack_veggie2)

if unit_price_veggie and not session.query(Inventory).filter_by(item_id=unit_price_veggie.id).first():
    inventory_unit_price_veggie = Inventory(item_id=unit_price_veggie.id, quantity=45)
    session.add(inventory_unit_price_veggie)

if unit_price_veggie2 and not session.query(Inventory).filter_by(item_id=unit_price_veggie2.id).first():
    inventory_unit_price_veggie2 = Inventory(item_id=unit_price_veggie2.id, quantity=40)
    session.add(inventory_unit_price_veggie2)

if premade_box and not session.query(Inventory).filter_by(item_id=premade_box.id).first():
    inventory_premade_box = Inventory(item_id=premade_box.id, quantity=10)
    session.add(inventory_premade_box)

if premade_box2 and not session.query(Inventory).filter_by(item_id=premade_box2.id).first():
    inventory_premade_box2 = Inventory(item_id=premade_box2.id, quantity=8)
    session.add(inventory_premade_box2)

# 提交事务
session.commit()

print("库存数据插入成功！")

