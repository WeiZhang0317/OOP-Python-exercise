from sqlalchemy.orm import sessionmaker
from db_config import engine
from models.customer import Customer, CorporateCustomer
from models.person import Person
from models.staff import Staff
from models.order import Order, OrderLine
from models.payment import Payment, CreditCardPayment, DebitCardPayment
from models.item import Veggie, WeightedVeggie, PackVeggie, UnitPriceVeggie, PremadeBox

# 创建会话
Session = sessionmaker(bind=engine)
session = Session()

# 依次删除每个表的数据
session.query(OrderLine).delete()
session.query(Order).delete()
session.query(CreditCardPayment).delete()
session.query(DebitCardPayment).delete()
session.query(Payment).delete()
session.query(PremadeBox).delete()
session.query(UnitPriceVeggie).delete()
session.query(PackVeggie).delete()
session.query(WeightedVeggie).delete()
session.query(Veggie).delete()
session.query(Staff).delete()
session.query(CorporateCustomer).delete()
session.query(Customer).delete()
session.query(Person).delete()

# 提交更改
session.commit()
print("所有表中的数据已被清空！")
