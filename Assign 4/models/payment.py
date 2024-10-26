from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from models import db  # 从 models/__init__.py 导入 db 实例
from .customer import Customer  # 确保正确导入 Customer 模型
import re

class Payment(db.Model):  # 使用 db.Model 代替 Base
    """!
    Represents a payment made for an order in the Fresh Harvest Veggies system.
    """
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    payment_amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, default=datetime.now)
    customer_id = Column(Integer, ForeignKey('customers.cust_id'), nullable=False)

    customer = relationship("Customer", back_populates="list_of_payments")

    def __init__(self, payment_amount: float, customer: Customer, payment_date: datetime = None):
        self.payment_amount = payment_amount
        self.customer_id = customer.cust_id  # 通过 Customer 对象设置 customer_id
        self.payment_date = payment_date if payment_date else datetime.now()

    def get_payment_details(self) -> str:
        """!
        Returns a string describing the payment details.
        @return: A string containing the payment ID, amount, and date.
        """
        return (f"Payment ID: {self.id}, Amount: ${self.payment_amount:.2f}, "
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

    __mapper_args__ = {
        'polymorphic_identity': 'credit_card'
    }

    def __init__(self, payment_amount: float, customer: Customer, card_number: str, card_type: str, card_expiry_date: str, payment_date: datetime = None):
        super().__init__(payment_amount, customer, payment_date)
        self.card_number = card_number
        self.card_type = card_type
        self.card_expiry_date = card_expiry_date
    
    @staticmethod
    def validate_credit_card(card_number: str, card_expiry_date: str, cvv: str) -> bool:
            """Validates credit card details including card number, expiry date, and CVV."""
            if not re.fullmatch(r'\d{16}', card_number):
                raise ValueError('Invalid card number. It must be 16 digits.')
            
            if not re.fullmatch(r'(0[1-9]|1[0-2])/\d{4}', card_expiry_date):
                raise ValueError('Invalid expiry date format. Please use MM/YYYY.')
            
            if not re.fullmatch(r'\d{3}', cvv):
                raise ValueError('Invalid CVV. It must be 3 digits.')
            
            return True

    
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

    __mapper_args__ = {
        'polymorphic_identity': 'debit_card'
    }

    def __init__(self, payment_amount: float, customer: Customer, bank_name: str, debit_card_number: str, payment_date: datetime = None):
        super().__init__(payment_amount, customer, payment_date)
        self.bank_name = bank_name
        self.debit_card_number = debit_card_number

    def get_payment_details(self) -> str:
        """!
        Returns a string describing the debit card payment details, including bank name and masked card number.
        @return: A string containing the payment details.
        """
        masked_card = "**** **** **** " + self.debit_card_number[-4:]  # Masking card number for security
        return (f"Debit Card Payment - {super().get_payment_details()}, Bank Name: {self.bank_name}, "
                f"Card Number: {masked_card}")


    
    @staticmethod
    def validate_debit_card(debit_card_number: str) -> bool:
        """Validates debit card details including card number."""
        if not re.fullmatch(r'\d{16}', debit_card_number):
            raise ValueError('Invalid debit card number. It must be 16 digits.')
        return True