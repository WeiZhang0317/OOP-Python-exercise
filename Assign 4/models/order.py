from typing import List
from datetime import datetime
from .item import Item
from .customer import Customer
from enum import Enum

class OrderStatus(Enum):
    PENDING = "Pending"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    
class Order:
    """!
    Represents an order placed by a customer in the Fresh Harvest Veggies system.
    """

    def __init__(self, order_id: int, customer: Customer, items: List[Item], delivery: bool, payment_method: str) -> None:
        """!
        Constructor for the Order class.
        Initializes the order with a unique order ID, customer, items, delivery preference, and payment method.

        @param order_id: The unique identifier for the order.
        @param customer: The Customer object placing the order.
        @param items: A list of Item objects that the customer is ordering.
        @param delivery: A boolean indicating if the order is for delivery (True) or pickup (False).
        @param payment_method: The payment method used for the order (e.g., "credit", "debit", "account").
        """
        self.__order_id = order_id  # Private attribute to protect order ID
        self.customer = customer  # The customer who places the order
        self.list_of_items = items  # List of items in the order
        self.delivery = delivery  # Delivery preference
        self.payment_method = payment_method  # Payment method used
        self.__total_cost = 0.0  # Private total cost attribute, updated with add_item()
        self.order_status = OrderStatus.PENDING.value  # Default order status
        self.order_date = datetime.now()  # Set the order date to current datetime

    def add_item(self, item: Item) -> None:
        """!
        Adds an item to the order and updates the total cost.
        
        @param item: The Item object to be added to the order.
        """
        if item not in self.list_of_items:
            self.list_of_items.append(item)
            self.__total_cost += item.get_price()  # Update total cost
            print(f"Item '{item.name}' added to the order.")
        else:
            print(f"Item '{item.name}' is already in the order.")

    def remove_item(self, item: Item) -> None:
        """!
        Removes an item from the order and updates the total cost.
        
        @param item: The Item object to be removed from the order.
        """
        if item in self.list_of_items:
            self.list_of_items.remove(item)
            self.__total_cost -= item.get_price()
            print(f"Item '{item.name}' removed from the order.")
        else:
            print(f"Item '{item.name}' not found in the order.")

    def calculate_total(self) -> float:
        """!
        Calculates the total cost of the order, including any delivery fees if applicable.
        
        If delivery is True, an extra delivery fee is added.

        @return: A float representing the total cost of the order.
        """
        delivery_fee = 5.0 if self.delivery else 0.0  # Delivery fee if applicable
        total = sum([item.get_price() for item in self.list_of_items]) + delivery_fee
        self.__total_cost = total  # Update the total cost attribute
        return self.__total_cost

    def process_payment(self, amount: float) -> bool:
        """!
        Processes a payment for the order.
        Ensures the payment is sufficient to cover the total cost.

        @param amount: The amount paid towards the order.
        @return: True if the payment was successful, otherwise False.
        """
        total_cost = self.calculate_total()
        if amount >= total_cost:
            # Update customer balance and payment record (assuming a Customer method for this)
            self.customer.add_payment(amount)  # Log payment in customer's history
            self.customer.update_balance(-total_cost)  # Deduct order cost from customer's balance
            self.order_status = "Paid"
            print(f"Payment of {amount} accepted for Order ID {self.__order_id}. Order is now marked as 'Paid'.")
            return True
        else:
            print(f"Payment of {amount} is insufficient for Order ID {self.__order_id}. Total cost is {total_cost}.")
            return False

    def get_order_id(self) -> int:
        """!
        Returns the unique order ID.

        @return: The unique identifier for the order.
        """
        return self.__order_id

    def get_total_cost(self) -> float:
        """!
        Returns the total cost of the order.

        @return: The total cost of the order as a float.
        """
        return self.__total_cost

    def set_order_status(self, status: str) -> None:
        """!
        Sets the order status.

        @param status: The status to set for the order (e.g., 'Pending', 'Shipped', 'Delivered').
        """
        self.order_status = status

    def get_order_status(self) -> str:
        """!
        Returns the current status of the order.

        @return: The order status as a string.
        """
        return self.order_status

    def __str__(self) -> str:
        """!
        Returns a string representation of the order with its details.
        
        @return: A string describing the order.
        """
        item_details = ', '.join([item.name for item in self.list_of_items])
        return (f"Order ID: {self.__order_id}, Customer: {self.customer.get_full_name()}, "
                f"Items: [{item_details}], Total Cost: ${self.__total_cost:.2f}, "
                f"Delivery: {'Yes' if self.delivery else 'No'}, Status: {self.order_status}, "
                f"Date: {self.order_date.strftime('%Y-%m-%d')}")

