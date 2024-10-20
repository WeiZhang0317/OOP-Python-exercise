from db_config import engine  # 继续导入 engine，如果其他地方用到
from models import db  # 导入 db 实例
from models.customer import Customer, CorporateCustomer
from models.item import Item, Veggie, WeightedVeggie, PackVeggie, UnitPriceVeggie, PremadeBox  
from models.order import Order, OrderLine
from models.person import Person
from models.staff import Staff
from models.payment import Payment, CreditCardPayment, DebitCardPayment
from app import app  # 假设你的 Flask 应用是定义在 app.py 中的

# 使用应用上下文
with app.app_context():
    db.create_all()  # 在应用上下文中创建所有表

if __name__ == "__main__":
    print("Database tables created!")
