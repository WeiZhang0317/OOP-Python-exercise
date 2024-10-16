# main.py
# For table creation

from db_config import engine, Base  
from models.customer import Customer,CorporateCustomer
from models.item import Item, Veggie, WeightedVeggie, PackVeggie, UnitPriceVeggie, PremadeBox  
from models.order import Order, OrderLine
from models.person import Person
from models.staff import Staff
from models.payment import Payment, CreditCardPayment, DebitCardPayment



Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    print("Database tables created!")

