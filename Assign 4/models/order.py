from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship, joinedload
from models import db  # Import db instance from models/__init__.py
from typing import List
from datetime import datetime, timezone
from enum import Enum
from .customer import Customer
from .item import Item
import random

# models/order.py

class Cart:
    def __init__(self, session_cart):
        """Initialize the cart using data from the session."""
        self.cart = session_cart if session_cart else []

    def add_item(self, item, quantity):
        """Add an item to the cart or update quantity if already present."""
        item_in_cart = next((cart_item for cart_item in self.cart if cart_item['item_id'] == item.id), None)

        if item_in_cart:
            item_in_cart['quantity'] += quantity
            item_in_cart['line_total'] = item_in_cart['price'] * item_in_cart['quantity']
        else:
            new_cart_item = {
                'item_id': item.id,
                'name': item.name,
                'price': item.get_price(),
                'quantity': quantity,
                'type': item.type,
                'line_total': item.get_price() * quantity
            }
            self.cart.append(new_cart_item)

    def remove_item(self, item_id):
        """Remove an item from the cart based on its ID."""
        self.cart = [item for item in self.cart if item['item_id'] != item_id]

    def get_total_price(self):
        """Calculate and return the total price of items in the cart."""
        return sum(item['line_total'] for item in self.cart)

    def get_cart(self):
        """Return the list of items in the cart."""
        return self.cart


class OrderStatus(Enum):
    """Enum representing different statuses an order can have."""
    PENDING = "Pending"
    SHIPPED = "Shipped"
    PAID = "Paid"
    CANCELED = "Canceled"

    @classmethod
    def has_value(cls, val: str):
        """Check if the given value is a valid status in the Enum."""
        return val in cls._value2member_map_

    @classmethod
    def get_next_status(cls, val: str):
        """Return the next logical status for the order, if applicable."""
        if val == cls.PENDING.value:
            return cls.PAID.value
        elif val == cls.PAID.value:
            return cls.SHIPPED.value
        elif val == cls.SHIPPED.value:
            return cls.CANCELED.value
        return None


class OrderLine(db.Model):
    """Represents a single item line in an order, including quantity and total cost."""
    __tablename__ = 'order_lines'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    item_id = Column(Integer, ForeignKey('items.id'))
    quantity = Column(Integer, nullable=False)
    line_total = Column(Float, nullable=False)

    # Relationships to Order and Item models
    order = relationship("Order", back_populates="list_of_order_lines")
    item = relationship("Item", back_populates="order_lines")

    def __init__(self, order_id: int, item_id: int, quantity: int, line_total: float):
        self.order_id = order_id
        self.item_id = item_id
        self.quantity = quantity
        self.line_total = line_total

    def get_line_total(self) -> float:
        """Calculate and return the total cost for this order line."""
        return self.item.calculate_total(self.quantity)

    def __str__(self) -> str:
        return f"Item: {self.item.name}, Quantity: {self.quantity}, Line Total: ${self.get_line_total():.2f}"


class Order(db.Model):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_number = Column(Integer, unique=True, nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.cust_id'))
    order_date = Column(DateTime, default=datetime.now(timezone.utc))
    order_status = Column(String(50), nullable=False)
    total_cost = Column(Float, nullable=False)
    staff_id = Column(Integer, ForeignKey('staff.id'))

    list_of_order_lines = relationship("OrderLine", back_populates="order")
    customer = relationship("Customer", back_populates="list_of_orders")
    staff = relationship("Staff", back_populates="list_of_orders")

    def __init__(self, order_number: int, customer_id: int, staff_id: int, order_status: str, total_cost: float):
        self.order_number = order_number
        self.customer_id = customer_id
        self.staff_id = staff_id
        self.order_date = datetime.now()
        self.order_status = order_status
        self.total_cost = total_cost

    def add_order_line(self, order_line: OrderLine) -> None:
        """Add an OrderLine item to the order."""
        if order_line not in self.list_of_order_lines:
            self.list_of_order_lines.append(order_line)

    def remove_order_line(self, order_line: OrderLine) -> None:
        """Remove an OrderLine item from the order."""
        if order_line in self.list_of_order_lines:
            self.list_of_order_lines.remove(order_line)

    def get_total_cost(self) -> float:
        """Calculate the total cost of the order from all order lines."""
        total = sum([line.get_line_total() for line in self.list_of_order_lines])
        return total

    def set_order_status(self, status: str) -> None:
        """Set the order status if valid."""
        if OrderStatus.has_value(status):
            self.order_status = status

    def get_order_status(self) -> str:
        """Return the current status of the order."""
        return self.order_status

    @staticmethod
    def generate_unique_order_number():
        """Generate a random, unique 4-digit order number."""
        while True:
            order_number = random.randint(1000, 9999)
            existing_order = db.session.query(Order).filter_by(order_number=order_number).first()
            if not existing_order:
                return order_number

    def get_order_lines(self):
        """Retrieve all order lines associated with this order, with item details."""
        order_lines = db.session.query(OrderLine).options(joinedload(OrderLine.item)).filter_by(order_id=self.id).all()
        
        # Debug output for verifying order lines
        print("Order Lines:")  
        for line in order_lines:
            print(f"Item: {line.item.name}, Quantity: {line.quantity}, Line Total: ${line.line_total}")

        return order_lines
    
    def calculate_total_with_delivery(self, delivery_option: str) -> float:
        """Calculate the total cost, adding a delivery fee if applicable."""
        delivery_fee = 10.00 if delivery_option == 'delivery' else 0.00
        return self.total_cost + delivery_fee

    def update_status(self, new_status: str):
        """Update the status of the order and save it to the database."""
        self.order_status = new_status
        db.session.commit()

    def __str__(self) -> str:
        """Return a string representation of the order details."""
        order_line_details = ', '.join([str(line) for line in self.list_of_order_lines])
        return (f"Order Number: {self.order_number}, Customer: {self.customer.get_full_name()}, "
                f"Order Lines: [{order_line_details}], Total Cost: ${self.get_total_cost():.2f}, "
                f"Status: {self.order_status}, Date: {self.order_date.strftime('%Y-%m-%d')}")
