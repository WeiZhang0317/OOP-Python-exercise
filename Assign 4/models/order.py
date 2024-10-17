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
    
     # Relationship with Order and Item
    order = relationship("Order", back_populates="list_of_order_lines")  
    item = relationship("Item", back_populates="order_lines") 
    
    def __init__(self, order_id: int, item_id: int, quantity: int, line_total: float):
        """!
        Initializes an OrderLine object with the provided details.
        @param order_id: The ID of the order associated with this line item.
        @param item_id: The ID of the item in this line item.
        @param quantity: The quantity of the item ordered.
        @param line_total: The total cost for this line item.
        """
        self.order_id = order_id
        self.item_id = item_id
        self.quantity = quantity
        self.line_total = line_total

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
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_number = Column(Integer, unique=True, nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.cust_id'))
    order_date = Column(DateTime, default=datetime.now)
    order_status = Column(String(50), nullable=False)
    total_cost = Column(Float, nullable=False)

    staff_id = Column(Integer, ForeignKey('staff.id'))

    list_of_order_lines = relationship("OrderLine", back_populates="order")
    customer = relationship("Customer", back_populates="list_of_orders")
    staff = relationship("Staff", back_populates="list_of_orders")

    def __init__(self, order_number: int, customer_id: int, staff_id: int, order_status: str, total_cost: float):
        """!
        Initializes the order with a unique order number, customer, staff, order status, and total cost.
        The order date is automatically set to the current date and time.
        """
       
        self.order_number = order_number
        self.customer_id = customer_id  # Sets the foreign key to customer
        self.staff_id = staff_id
        self.order_date = datetime.now()  # Automatically set to the current date and time
        self.order_status = order_status
        self.total_cost = total_cost

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
