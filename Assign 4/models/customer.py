# customer.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from db_config import Base
from .person import Person


class Customer(Base,Person):
    __tablename__ = 'customers' 
    cust_id = Column(Integer, primary_key=True, index=True) 
    cust_address = Column(String(100), nullable=False) 
    cust_balance = Column(Float, default=0.0)  
    max_owing = Column(Float, default=100.0)  
    
    list_of_orders = []  # A list to track customer's orders
    list_of_payments = []  # A list to track customer's payments

    """!
    Represents a customer who can place orders and make payments.
    Inherits from the Person class and adds additional attributes and methods specific to customers.
    """

    def __init__(self, first_name: str, last_name: str, username: str, password: str, cust_address: str, cust_id: int, cust_balance: float = 0.0):
        """!
        Initializes the Customer class with additional attributes specific to customers.
        @param first_name: The first name of the customer.
        @param last_name: The last name of the customer.
        @param username: The username of the customer for login.
        @param password: The password of the customer.
        @param cust_address: The address of the customer.
        @param cust_id: A unique identifier for the customer.
        @param cust_balance: The initial balance amount of the customer, default is 0.0.
        """
        super().__init__(first_name, last_name, username, password)  # Call the parent class (Person) constructor
        self.cust_address = cust_address
        self.cust_id = cust_id
        self.cust_balance = cust_balance
        self.max_owing = 100.0  # Maximum amount the customer can owe before being restricted from placing new orders
        self.list_of_orders = []  # A list to track customer's orders
        self.list_of_payments = []  # A list to track customer's payments

    def place_order(self, order):
        """!
        Places an order for the customer.
        @param order: The order to be placed.
        """
        if self.cust_balance <= self.max_owing:
            self.list_of_orders.append(order)
            print(f"Order {order.order_number} placed successfully.")
        else:
            print("Order cannot be placed. Outstanding balance exceeds maximum owing limit.")

    def make_payment(self, payment):
        """!
        Makes a payment and adds it to the customer's payment history.
        @param payment: The payment to be made.
        """
        self.list_of_payments.append(payment)
        self.cust_balance -= payment.payment_amount
        print(f"Payment of {payment.payment_amount} made successfully. New balance: {self.cust_balance}")

    def view_order_history(self):
        """!
        Displays the customer's order history.
        """
        if not self.list_of_orders:
            print("No orders found in your history.")
        else:
            print("Order History:")
            for order in self.list_of_orders:
                print(order)

    def view_payment_history(self):
        """!
        Displays the customer's payment history.
        """
        if not self.list_of_payments:
            print("No payments found in your history.")
        else:
            print("Payment History:")
            for payment in self.list_of_payments:
                print(payment)

    def get_customer_details(self) -> str:
        """!
        Returns a string containing the customer's details.
        @return: A formatted string with customer information.
        """
        return (f"Customer ID: {self.cust_id}\n"
                f"Name: {self.get_full_name()}\n"
                f"Address: {self.cust_address}\n"
                f"Balance: {self.cust_balance}\n"
                f"Max Owing Limit: {self.max_owing}\n"
                f"Number of Orders: {len(self.list_of_orders)}\n"
                f"Number of Payments: {len(self.list_of_payments)}")

    def __str__(self) -> str:
        """!
        Returns a string representation of the customer.
        @return: A string describing the customer.
        """
        return f"Customer ID: {self.cust_id}, Name: {self.get_full_name()}, Balance: {self.cust_balance}"


# Additional specialized Customer classes
class CorporateCustomer(Customer):
    """!
    Represents a corporate customer, inheriting from the Customer class and adding corporate-specific attributes.
    """
    __tablename__ = 'corporate_customers'
    
    cust_id = Column(Integer, ForeignKey('customers.cust_id'), primary_key=True)  
    discount_rate = Column(Float, default=0.10)  
    max_credit = Column(Float, default=1000.0) 
    min_balance = Column(Float, default=500.0)  
    
    def __init__(self, first_name: str, last_name: str, username: str, password: str, cust_address: str, cust_id: int,
                 cust_balance: float = 0.0, discount_rate: float = 0.10, max_credit: float = 1000.0, min_balance: float = 500.0):
        """!
        Initializes the CorporateCustomer class with additional attributes.
        @param discount_rate: Discount rate applicable to corporate customers.
        @param max_credit: Maximum credit allowed for corporate customers.
        @param min_balance: Minimum balance to maintain before placing new orders.
        """
        super().__init__(first_name, last_name, username, password, cust_address, cust_id, cust_balance)
        self.discount_rate = discount_rate
        self.max_credit = max_credit
        self.min_balance = min_balance

    def place_order(self, order):
        """!
        Places an order for the corporate customer with a discount.
        Applies discount and checks if minimum balance is maintained.
        """
        if self.cust_balance >= self.min_balance:
            order.order_total *= (1 - self.discount_rate)  # Apply discount to the order total
            super().place_order(order)
        else:
            print("Order cannot be placed. Customer balance is below the required minimum balance.")

    def get_corporate_details(self) -> str:
        """!
        Returns a string containing the corporate customer's details.
        @return: A formatted string with corporate customer information.
        """
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
        """!
        Returns a string representation of the corporate customer.
        @return: A string describing the corporate customer.
        """
        return f"Corporate Customer ID: {self.cust_id}, Name: {self.get_full_name()}, Balance: {self.cust_balance}, Discount: {self.discount_rate * 100}%"

