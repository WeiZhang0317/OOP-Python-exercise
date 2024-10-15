# order.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db_config import Base 
from typing import List
from datetime import datetime
from enum import Enum
from .customer import Customer
from .item import Item


class OrderStatus(Enum):
    """!
    Enum representing different statuses of an order.
    """
    PENDING = "Pending"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    PAID = "Paid"
    CANCELED = "Canceled"


class OrderLine(Base):
    """!
    Represents a single line item in an order, associated with a specific item and quantity.
    """
    __tablename__ = 'order_lines'

    id = Column(Integer, primary_key=True, autoincrement=True)  
    order_id = Column(Integer, ForeignKey('orders.id'))
    item_id = Column(Integer, ForeignKey('items.id'))  
    quantity = Column(Integer, nullable=False) 
    line_total = Column(Float, nullable=False)  
    
    def __init__(self, item: Item, quantity: int):
        """!
        Initializes the OrderLine with a specific item and quantity.

        @param item: The Item object being ordered.
        @param quantity: The number of units of the item.
        """
        self.item = item  # The item being ordered
        self.quantity = quantity  # The number of units of the item

    def get_line_total(self) -> float:
        """!
        Calculates and returns the total cost for this line item.

        @return: The total cost of this line item as a float.
        """
        return self.item.get_price() * self.quantity

    def __str__(self) -> str:
        """!
        Returns a string representation of the order line with item details and quantity.

        @return: A string describing the order line.
        """
        return f"Item: {self.item.name}, Quantity: {self.quantity}, Line Total: ${self.get_line_total():.2f}"


class Order(Base):
    """!
    Represents an order placed by a customer in the Fresh Harvest Veggies system.
    """
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True) 
    order_number = Column(Integer, unique=True, nullable=False) 
    customer_id = Column(Integer, ForeignKey('customers.cust_id')) 
    order_date = Column(DateTime, default=datetime) 
    order_status = Column(String(50), nullable=False)
    total_cost = Column(Float, nullable=False) 

    list_of_order_lines = relationship("OrderLine", backref="order")
    
    def __init__(self, order_number: int, order_customer: Customer, list_of_order_lines: List[OrderLine], order_status: str = OrderStatus.PENDING.value):
        """!
        Initializes the order with a unique order number, customer, order lines, and order status.

        @param order_number: The unique identifier for the order.
        @param order_customer: The Customer object placing the order.
        @param list_of_order_lines: A list of OrderLine objects that the customer is ordering.
        @param order_status: The initial status of the order, defaults to 'Pending'.
        """
        self.order_number = order_number  # Order number (unique)
        self.order_customer = order_customer  # The customer who places the order
        self.list_of_order_lines = list_of_order_lines  # List of order lines in the order
        self.order_status = order_status  # Initial order status
        self.order_date = datetime.now()  # Set the order date to current datetime

    def add_order_line(self, order_line: OrderLine) -> None:
        """!
        Adds an order line to the order.

        @param order_line: The OrderLine object to be added to the order.
        """
        if order_line not in self.list_of_order_lines:
            self.list_of_order_lines.append(order_line)

    def remove_order_line(self, order_line: OrderLine) -> None:
        """!
        Removes an order line from the order.

        @param order_line: The OrderLine object to be removed from the order.
        """
        if order_line in self.list_of_order_lines:
            self.list_of_order_lines.remove(order_line)

    def get_total_cost(self) -> float:
        """!
        Calculates and returns the total cost of the order, based on all order line totals.

        @return: The total cost of the order as a float.
        """
        total = sum([line.get_line_total() for line in self.list_of_order_lines])
        return total

    def set_order_status(self, status: str) -> None:
        """!
        Sets the order status.

        @param status: The status to set for the order (e.g., 'Pending', 'Shipped', 'Delivered', 'Paid').
        """
        if status in OrderStatus._value2member_map_:
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
        order_line_details = ', '.join([str(line) for line in self.list_of_order_lines])
        return (f"Order Number: {self.order_number}, Customer: {self.order_customer.get_full_name()}, "
                f"Order Lines: [{order_line_details}], Total Cost: ${self.get_total_cost():.2f}, "
                f"Status: {self.order_status}, Date: {self.order_date.strftime('%Y-%m-%d')}")
