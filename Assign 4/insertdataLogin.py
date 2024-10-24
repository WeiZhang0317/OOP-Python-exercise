from sqlalchemy.orm import sessionmaker
from db_config import engine
from models.customer import Customer, CorporateCustomer
from models.person import Person
from models.staff import Staff
from datetime import datetime

# 创建session
Session = sessionmaker(bind=engine)
session = Session()

# 检查并插入第一个 Customer
if not session.query(Person).filter_by(username="alice_wonder").first():
    customer1 = Customer(
        first_name="Alice",
        last_name="Wonder",
        username="alice_wonder",
        password="CustomerPass123",  # 明文密码，不进行加密
        cust_balance=100,
        cust_address="123 Fantasy Road, Wonderland"
    )
    session.add(customer1)

# 检查并插入第二个 Customer
if not session.query(Person).filter_by(username="bob_builder").first():
    customer2 = Customer(
        first_name="Bob",
        last_name="Builder",
        username="bob_builder",
        password="CustomerPass123",  # 明文密码，不进行加密
        cust_balance=200,
        cust_address="456 Construction Ave, Buildtown"
    )
    session.add(customer2)

# 检查并插入 CorporateCustomer
if not session.query(Person).filter_by(username="corporate_karen").first():
    corporate_customer = CorporateCustomer(
        first_name="Karen",
        last_name="Corporate",
        username="corporate_karen",
        password="CorporatePass456",  # 明文密码，不进行加密
        cust_address="789 Business Blvd, Corporatia",
        cust_balance=200,
        discount_rate=0.15,  # 自定义折扣率
        max_credit=2000.0,   # 自定义信用额度
        min_balance=1000.0   # 自定义最低余额
    )
    session.add(corporate_customer)

# 检查并插入 Staff
if not session.query(Person).filter_by(username="staff_john").first():
    staff = Staff(
        first_name="John",
        last_name="Staffer",
        username="staff_john",
        password="StaffPass789",  # 明文密码，不进行加密
        dept_name="Sales"
    )
    session.add(staff)

# 提交到数据库
session.commit()
session.close()