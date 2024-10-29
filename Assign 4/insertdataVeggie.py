from sqlalchemy.orm import sessionmaker
from db_config import engine
from models.customer import Customer, CorporateCustomer
from models.person import Person
from models.staff import Staff
from models.order import Order, OrderLine, OrderStatus
from models.item import Item, Veggie, WeightedVeggie, PackVeggie, UnitPriceVeggie, PremadeBox,Inventory
from models.payment import Payment, CreditCardPayment, DebitCardPayment

from datetime import datetime
import random


Session = sessionmaker(bind=engine)
session = Session()


if not session.query(Veggie).filter_by(name="Capsicum").first():
    veggie1 = Veggie(name="Capsicum", price=2.0, veg_name="Capsicum")
    session.add(veggie1)

if not session.query(Veggie).filter_by(name="Cucumber").first():
    veggie2 = Veggie(name="Cucumber", price=1.5, veg_name="Cucumber")
    session.add(veggie2)

if not session.query(Veggie).filter_by(name="Broccoli").first():
    veggie3 = Veggie(name="Broccoli", price=4.0, veg_name="Broccoli")
    session.add(veggie3)

if not session.query(Veggie).filter_by(name="Lettuce").first():
    veggie4 = Veggie(name="Lettuce", price=3.5, veg_name="Lettuce")
    session.add(veggie4)


if not session.query(WeightedVeggie).filter_by(name="Potato").first():
    weighted_veggie = WeightedVeggie(name="Potato", price=1.5, veg_name="Potato", weight_per_kilo=1.5, unit_type="kg")
    session.add(weighted_veggie)

if not session.query(WeightedVeggie).filter_by(name="Sweet Potato").first():
    weighted_veggie2 = WeightedVeggie(name="Sweet Potato", price=2.0, veg_name="Sweet Potato", weight_per_kilo=2.0, unit_type="kg")
    session.add(weighted_veggie2)


if not session.query(PackVeggie).filter_by(name="Tomato Pack").first():
    pack_veggie = PackVeggie(name="Tomato Pack", price=5.0, veg_name="Tomato", num_in_pack=3)
    session.add(pack_veggie)

if not session.query(PackVeggie).filter_by(name="Mushroom Pack").first():
    pack_veggie2 = PackVeggie(name="Mushroom Pack", price=6.0, veg_name="Mushroom", num_in_pack=7)
    session.add(pack_veggie2)


if not session.query(UnitPriceVeggie).filter_by(name="Bok choy").first():
    unit_price_veggie = UnitPriceVeggie(name="Bok choy", price=5.5, veg_name="Bok choy", price_per_unit=5.5, unit_type="bunch")
    session.add(unit_price_veggie)

if not session.query(UnitPriceVeggie).filter_by(name="Spring onion").first():
    unit_price_veggie2 = UnitPriceVeggie(name="Spring onion", price=3.0, veg_name="Spring onion", price_per_unit=3.0, unit_type="bunch")
    session.add(unit_price_veggie2)


if not session.query(PremadeBox).filter_by(name="Small Veggie Box").first():
    small_premade_box = PremadeBox(name="Small Veggie Box", price=15.0, box_size="small")
    session.add(small_premade_box)

if not session.query(PremadeBox).filter_by(name="Medium Veggie Box").first():
    medium_premade_box = PremadeBox(name="Medium Veggie Box", price=20.0, box_size="medium")
    session.add(medium_premade_box)

if not session.query(PremadeBox).filter_by(name="Large Veggie Box").first():
    large_premade_box = PremadeBox(name="Large Veggie Box", price=30.0, box_size="large")
    session.add(large_premade_box)

session.commit()


items = session.query(Item).all()
for item in items:
    quantity = random.randint(80, 200)
    
  
    inventory_entry = Inventory(item_id=item.id, quantity=quantity)
    session.add(inventory_entry)

session.commit()

