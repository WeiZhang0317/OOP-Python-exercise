# payment.py
from sqlalchemy import Column, Integer, String, Float, DateTime,ForeignKey
from datetime import datetime
from db_config import Base
from sqlalchemy.orm import relationship

class Payment(Base): 
    """!
    Represents a payment made for an order in the Fresh Harvest Veggies system.
    """
    __tablename__ = 'payments' 
    id = Column(Integer, primary_key=True, autoincrement=True)  
    payment_amount = Column(Float, nullable=False) 
    payment_date = Column(DateTime, default=datetime.now) 
    
    customer_id = Column(Integer, ForeignKey('customers.cust_id'), nullable=False)

    customer = relationship("Customer", back_populates="list_of_payments")

    def __init__(self, payment_id: int, payment_amount: float, payment_date: datetime = None):
        """!
        Constructor for the Payment class.

        @param payment_id: The unique identifier for the payment.
        @param payment_amount: The amount paid.
        @param payment_date: The date when the payment was made. If not provided, defaults to current date and time.
        """
        self.payment_id = payment_id  # Unique payment identifier
        self.payment_amount = payment_amount  # Payment amount
        self.payment_date = payment_date if payment_date else datetime.now()  # Payment date, defaults to now

    def get_payment_details(self) -> str:
        """!
        Returns a string describing the payment details.

        @return: A string containing the payment ID, amount, and date.
        """
        return (f"Payment ID: {self.payment_id}, Amount: ${self.payment_amount:.2f}, "
                f"Date: {self.payment_date.strftime('%Y-%m-%d %H:%M:%S')}")


class CreditCardPayment(Payment):
    """!
    Represents a payment made using a credit card. Inherits from Payment.
    """
    __tablename__ = 'credit_card_payments'
    
    id = Column(Integer, ForeignKey('payments.id'), primary_key=True)
    card_number = Column(String(16), nullable=False)  
    card_type = Column(String(20), nullable=False)  
    card_expiry_date = Column(String(7), nullable=False) 


    def __init__(self,  payment_amount: float, card_number: str, card_type: str, card_expiry_date: str, payment_date: datetime = None):
        """!
        Constructor for the CreditCardPayment class.

        @param payment_id: The unique identifier for the payment.
        @param payment_amount: The amount paid.
        @param card_number: The credit card number used for the payment.
        @param card_type: The type of credit card (e.g., Visa, MasterCard).
        @param card_expiry_date: The expiration date of the credit card.
        @param payment_date: The date when the payment was made. If not provided, defaults to current date and time.
        """
        super().__init__(payment_amount, payment_date)
        self.card_number = card_number  # Credit card number
        self.card_type = card_type  # Type of credit card
        self.card_expiry_date = card_expiry_date  # Expiration date of the credit card

    def validate_card(self) -> bool:
        """!
        Validates the credit card details.
        
        This is a simplified version and would normally involve more complex checks.
        
        @return: True if the card number and expiry date are valid, otherwise False.
        """
        # Check if the card number is 16 digits and if the card has not expired
        if len(self.card_number) == 16 and self.card_expiry_date > datetime.now().strftime("%Y-%m"):
            return True
        return False

    def get_payment_details(self) -> str:
        """!
        Returns a string describing the credit card payment details, including card type and masked card number.

        @return: A string containing the payment details.
        """
        masked_card = "**** **** **** " + self.card_number[-4:]  # Masking card number for security
        return (f"Credit Card Payment - {super().get_payment_details()}, Card Type: {self.card_type}, "
                f"Card Number: {masked_card}, Expiry Date: {self.card_expiry_date}")


class DebitCardPayment(Payment):
    """!
    Represents a payment made using a debit card. Inherits from Payment.
    """  
    
    __tablename__ = 'debit_card_payments'


    id = Column(Integer, ForeignKey('payments.id'), primary_key=True) 
    bank_name = Column(String(50), nullable=False)  
    debit_card_number = Column(String(16), nullable=False) 

    def __init__(self, payment_amount: float, bank_name: str, debit_card_number: str, payment_date: datetime = None):
        """!
        Constructor for the DebitCardPayment class.

        @param payment_id: The unique identifier for the payment.
        @param payment_amount: The amount paid.
        @param bank_name: The bank associated with the debit card.
        @param debit_card_number: The debit card number used for the payment.
        @param payment_date: The date when the payment was made. If not provided, defaults to current date and time.
        """
        super().__init__(payment_amount, payment_date)
        self.bank_name = bank_name  # Bank name associated with the debit card
        self.debit_card_number = debit_card_number  # Debit card number

    def validate_card(self) -> bool:
        """!
        Validates the debit card details.

        This is a simplified version and would normally involve more complex checks.

        @return: True if the debit card number is valid, otherwise False.
        """
        return len(self.debit_card_number) == 16  # Simple check for 16-digit card number

    def get_payment_details(self) -> str:
        """!
        Returns a string describing the debit card payment details, including bank name and masked card number.

        @return: A string containing the payment details.
        """
        masked_card = "**** **** **** " + self.debit_card_number[-4:]  # Masking card number for security
        return (f"Debit Card Payment - {super().get_payment_details()}, Bank Name: {self.bank_name}, "
                f"Card Number: {masked_card}")
