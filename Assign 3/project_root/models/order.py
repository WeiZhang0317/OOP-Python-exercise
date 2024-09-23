from typing import List
from .item import Item
from .customer import Customer

class Order:
    """!
    Represents an order placed by a customer in the Fresh Harvest Veggies system.
    """

    def __init__(self, orderId: int, customer: Customer, items: List[Item], delivery: bool, paymentMethod: str) -> None:
        """!
        Constructor for the Order class.
        Initializes the order with a unique order ID, customer, items, delivery preference, and payment method.
        @param orderId: The unique identifier for the order.
        @param customer: The Customer object placing the order.
        @param items: A list of Item objects that the customer is ordering.
        @param delivery: A boolean indicating if the order is for delivery (True) or pickup (False).
        @param paymentMethod: The payment method used for the order (e.g., "credit", "debit", "account").
        """
        self.__orderId = orderId  # Private
        self.customer = customer  # Public
        self.items = items  # Public
        self.delivery = delivery  # Public
        self.paymentMethod = paymentMethod  # Public
        self.__totalCost = 0.0  # Private

    def addItem(self, item: Item) -> None:
        """!
        Adds an item to the order.
        Updates the total cost of the order based on the added item.
        @param item: The Item object to be added to the order.
        """
        self.items.append(item)
        self.__totalCost += item.price  # Assuming each Item has a price attribute

    def calculateTotal(self) -> float:
        """!
        Calculates the total cost of the order, including any delivery fees if applicable.
        If delivery is True, an extra fee is added.
        @return A float representing the total cost of the order.
        """
        deliveryFee = 5.0 if self.delivery else 0.0  
        self.__totalCost += deliveryFee
        return self.__totalCost

    def processPayment(self, amount: float) -> bool:
        """!
        Processes a payment for the order.
        Ensures the payment is sufficient to cover the total cost.
        @param amount: The amount paid towards the order.
        @return True if the payment was successful, otherwise False.
        """
        if amount >= self.calculateTotal():
            print(f"Payment of {amount} accepted for Order ID {self.__orderId}.")
            return True
        else:
            print(f"Payment of {amount} insufficient for Order ID {self.__orderId}.")
            return False

    def getOrderId(self) -> int:
        """!
        Returns the unique order ID.
        @return The unique identifier for the order.
        """
        return self.__orderId  


    def getTotalCost(self) -> float:
        """!
        Returns the total cost of the order.
        @return The total cost of the order as a float.
        """
        return self.__totalCost  