from typing import List
from .item import Item
from .customer import Customer

class Order:
    """!
    Represents an order placed by a customer.
    """

    def __init__(self, orderId: int, customer: Customer, items: List[Item], delivery: bool, paymentMethod: str) -> None:
        """!
        Constructor for Order class.
        @param orderId: The unique identifier for the order.
        @param customer: The Customer object placing the order.
        @param items: A list of Item objects that the customer is ordering.
        @param delivery: A boolean indicating if the order is for delivery (True) or for pickup (False).
        @param paymentMethod: The payment method used for the order (e.g., "credit", "debit", "account").
        """
        pass


    def addItem(self, item: Item) -> None:
        """!
        Adds an item to the order.
        @param item: The Item object to be added to the order.
        """
        pass


    def calculateTotal(self) -> float:
        """!
        Calculates the total cost of the order, including any delivery fees if applicable.
        @return: A float representing the total cost of the order.
        """
        pass


    def processPayment(self, amount: float) -> bool:
        """!
        Processes a payment for the order.
        @param amount: The amount to pay towards the order.
        @return: True if the payment was successful, otherwise False.
        """
        pass
