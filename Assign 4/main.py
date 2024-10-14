# main.py

from db_config import engine, Base  
from models.customer import Customer,CorporateCustomer
from models.item import Item, Vegetable, WeightedVeggie, PackVeggie, UnitPriceVeggie, PremadeBox  
from models.order import Order, OrderLine
from models.person import Person
from models.order import Order
from models.payment import Payment, CreditCardPayment, DebitCardPayment



Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    print("Database tables created!")

