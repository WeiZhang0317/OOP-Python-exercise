from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from models import db  # Import db instance from models/__init__.py
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

    # Relationships to related tables
    list_of_payments = relationship("Payment", back_populates="customer")
    list_of_orders = relationship("Order", back_populates="customer")

    def __init__(self, first_name: str, last_name: str, username: str, password: str, cust_address: str, cust_balance: float = 0.0):
        super().__init__(first_name, last_name, username, password, role='customer')  # Default role is customer
        self.cust_address = cust_address
        self.cust_balance = cust_balance
        self.max_owing = 100.0
        self.list_of_orders = []  
        self.list_of_payments = []  
        
    def can_place_order_based_on_balance(self) -> bool:
        """Determine if the customer can place an order based on their balance status."""
        # Check if balance is within allowable limit when negative
        if self.cust_balance < 0:
            return abs(self.cust_balance) < self.max_owing
        return True  # Positive balance allows ordering
    
    def can_process_payment(self, payment_amount: float) -> bool:
        """Check if a payment can be processed without exceeding the maximum debt limit."""
        if self.cust_balance < 0 and abs(self.cust_balance) + payment_amount >= self.max_owing:
            return False
        return True
    
    def deduct_balance(self, payment_amount: float) -> bool:
        """Deducts the payment amount from the balance if within limit, returning success status."""
        if self.can_process_payment(payment_amount):
            self.cust_balance -= payment_amount
            return True
        return False

    def make_payment(self, payment):
        """Process a payment and deduct the amount from the balance if allowed."""
        if self.can_process_payment(payment.payment_amount):
            self.list_of_payments.append(payment)
            self.cust_balance -= payment.payment_amount
            print(f"Payment of {payment.payment_amount} was successful. New balance: {self.cust_balance}")
        else:
            print("Payment failed: Outstanding balance exceeds the maximum allowed debt limit.")

    def view_order_history(self):
        """Display the customer's order history or indicate none exist."""
        if not self.list_of_orders:
            print("No orders found in your history.")
        else:
            print("Order History:")
            for order in self.list_of_orders:
                print(order)

    def view_payment_history(self):
        """Display the customer's payment history or indicate none exist."""
        if not self.list_of_payments:
            print("No payments found in your history.")
        else:
            print("Payment History:")
            for payment in self.list_of_payments:
                print(payment)

    def get_customer_details(self) -> str:
        """Return formatted string of detailed customer information."""
        return (f"Customer ID: {self.cust_id}\n"
                f"Name: {self.get_full_name()}\n"
                f"Address: {self.cust_address}\n"
                f"Balance: {self.cust_balance}\n"
                f"Max Owing Limit: {self.max_owing}\n"
                f"Number of Orders: {len(self.list_of_orders)}\n"
                f"Number of Payments: {len(self.list_of_payments)}")
    
    @classmethod    
    def get_all_customers(cls):
        """Retrieve all customer records."""
        return db.session.query(cls).all()
    
    def __str__(self) -> str:
        return f"Customer ID: {self.cust_id}, Name: {self.get_full_name()}, Balance: {self.cust_balance}"

# CorporateCustomer class with additional attributes and order rules
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
        """Determine if the corporate customer can place an order based on balance requirements."""
        
        print(f"[DEBUG] Checking if customer with ID {self.cust_id} can place an order.")
        print(f"[DEBUG] Current balance: {self.cust_balance}, Minimum balance required: {self.min_balance}")

        # Prevent ordering if balance is negative
        if self.cust_balance < 0:
            print("[DEBUG] Cannot place order: Balance is negative.")
            return False
        
        # Allow ordering if balance meets or exceeds minimum required
        if self.cust_balance >= self.min_balance:
            print("[DEBUG] Order can be placed: Balance meets the minimum requirement.")
            return True
        else:
            print("[DEBUG] Cannot place order: Balance does not meet the minimum requirement.")
            return False

    def place_order(self, order):
        """Apply discount to order and place it if balance meets requirements."""
        if self.cust_balance >= self.min_balance:
            order.order_total *= (1 - self.discount_rate)  # Apply discount to order total
            super().place_order(order)
        else:
            print("Order cannot be placed. Customer balance is below the required minimum balance.")

    def get_corporate_details(self) -> str:
        """Return formatted string of detailed corporate customer information."""
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
