from db_config import engine  
from models import db  
from models.customer import Customer, CorporateCustomer
from models.item import Item, Veggie, WeightedVeggie, PackVeggie, UnitPriceVeggie, PremadeBox  
from models.order import Order, OrderLine
from models.person import Person
from models.staff import Staff
from models.payment import Payment, CreditCardPayment, DebitCardPayment
from app import app  


with app.app_context():
    db.create_all()  
if __name__ == "__main__":
    print("Database tables created!")
