from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from models import db  # 从 models/__init__.py 导入 db 实例
from .person import Person

class Customer(Person):
    __tablename__ = 'customers'
    cust_id = Column(Integer, ForeignKey('persons.id'), primary_key=True) 
    cust_address = Column(String(100), nullable=False)
    cust_balance = Column(Float, default=0.0)
    max_owing = Column(Float, default=100.0)
    __mapper_args__ = {
        'inherit_condition': cust_id == Person.id  
    }

    # Relationships
    list_of_payments = relationship("Payment", back_populates="customer")
    list_of_orders = relationship("Order", back_populates="customer")

    def __init__(self, first_name: str, last_name: str, username: str, password: str, cust_address: str, cust_balance: float = 0.0):
        super().__init__(first_name, last_name, username, password, role='customer')  # 设置默认角色
        self.cust_address = cust_address
        self.cust_balance = cust_balance
        self.max_owing = 100.0
        self.list_of_orders = []  
        self.list_of_payments = []  
        
    def can_place_order(self) -> bool:
        """检查私人客户的余额是否超过了允许的最大欠款额度"""
        return self.cust_balance <= self.max_owing


    def place_order(self, order):
        if self.can_place_order():
            self.list_of_orders.append(order)
            print(f"Order {order.order_number} placed successfully.")
        else:
            print("Order cannot be placed. Outstanding balance exceeds maximum owing limit.")

    def make_payment(self, payment):
        self.list_of_payments.append(payment)
        self.cust_balance -= payment.payment_amount
        print(f"Payment of {payment.payment_amount} made successfully. New balance: {self.cust_balance}")

    def view_order_history(self):
        if not self.list_of_orders:
            print("No orders found in your history.")
        else:
            print("Order History:")
            for order in self.list_of_orders:
                print(order)

    def view_payment_history(self):
        if not self.list_of_payments:
            print("No payments found in your history.")
        else:
            print("Payment History:")
            for payment in self.list_of_payments:
                print(payment)

    def get_customer_details(self) -> str:
        return (f"Customer ID: {self.cust_id}\n"
                f"Name: {self.get_full_name()}\n"
                f"Address: {self.cust_address}\n"
                f"Balance: {self.cust_balance}\n"
                f"Max Owing Limit: {self.max_owing}\n"
                f"Number of Orders: {len(self.list_of_orders)}\n"
                f"Number of Payments: {len(self.list_of_payments)}")

    def __str__(self) -> str:
        return f"Customer ID: {self.cust_id}, Name: {self.get_full_name()}, Balance: {self.cust_balance}"

# CorporateCustomer 类
class CorporateCustomer(Customer):
    __tablename__ = 'corporate_customers'
    
    cust_id = Column(Integer, ForeignKey('customers.cust_id'), primary_key=True)  
    discount_rate = Column(Float, default=0.10)  
    max_credit = Column(Float, default=1000.0) 
    min_balance = Column(Float, default=500.0)  
    
    def __init__(self, first_name: str, last_name: str, username: str, password: str, cust_address: str,
                 cust_balance: float = 0.0, discount_rate: float = 0.10, max_credit: float = 1000.0, min_balance: float = 500.0):
        super().__init__(first_name, last_name, username, password, cust_address, cust_balance)
        self.discount_rate = discount_rate
        self.max_credit = max_credit
        self.min_balance = min_balance
        
    def can_place_order(self) -> bool:
        """检查公司客户的余额是否足够下单"""
        return self.cust_balance >= self.min_balance    

    def place_order(self, order):
        if self.cust_balance >= self.min_balance:
            order.order_total *= (1 - self.discount_rate)  # 对订单应用折扣
            super().place_order(order)
        else:
            print("Order cannot be placed. Customer balance is below the required minimum balance.")

    def get_corporate_details(self) -> str:
        return (f"Corporate Customer ID: {self.cust_id}\n"
                f"Name: {self.get_full_name()}\n"
                f"Address: {self.cust_address}\n"
                f"Balance: {self.cust_balance}\n"
                f"Discount Rate: {self.discount_rate * 100}%\n"
                f"Max Credit: {self.max_credit}\n"
                f"Min Balance: {self.min_balance}\n"
                f"Number of Orders: {len(self.list_of_orders)}\n"
                f"Number of Payments: {len(self.list_of_payments)}")

    def __str__(self) -> str:
        return f"Corporate Customer ID: {self.cust_id}, Name: {self.get_full_name()}, Balance: {self.cust_balance}, Discount: {self.discount_rate * 100}%"
