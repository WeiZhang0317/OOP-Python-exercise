from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models import db  # 从 models/__init__.py 导入 db 实例
from typing import List
from datetime import datetime
from enum import Enum
from .customer import Customer
from .item import Item


# models/order.py

class Cart:
    def __init__(self, session_cart):
        """初始化购物车，传入session中的cart数据"""
        self.cart = session_cart if session_cart else []

    def add_item(self, item, quantity):
        """将商品添加到购物车"""
        item_in_cart = next((cart_item for cart_item in self.cart if cart_item['item_id'] == item.id), None)
        
        if item_in_cart:
            item_in_cart['quantity'] += quantity
            item_in_cart['line_total'] = item.calculate_total(item_in_cart['quantity'])
        else:
            new_cart_item = {
                'item_id': item.id,
                'name': item.name,
                'price': item.get_price(),
                'quantity': quantity,
                'line_total': item.calculate_total(quantity)
            }
            self.cart.append(new_cart_item)
    
    def remove_item(self, item_id):
        """从购物车中移除商品"""
        self.cart = [item for item in self.cart if item['item_id'] != item_id]

    def get_total_price(self):
        """计算购物车中商品的总价"""
        return sum(item['line_total'] for item in self.cart)

    def get_cart(self):
        """返回购物车列表"""
        return self.cart



class OrderStatus(Enum):
    """!
    Enum representing different statuses of an order.
    """
    PENDING = "Pending"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    PAID = "Paid"
    CANCELED = "Canceled"


class OrderLine(db.Model):  # 使用 db.Model 代替 Base
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
        return f"Item: {self.item.name}, Quantity: {self.quantity}, Line Total: ${self.get_line_total():.2f}"


class Order(db.Model):  # 使用 db.Model 代替 Base
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
        return (f"Order Number: {self.order_number}, Customer: {self.customer.get_full_name()}, "
                f"Order Lines: [{order_line_details}], Total Cost: ${self.get_total_cost():.2f}, "
                f"Status: {self.order_status}, Date: {self.order_date.strftime('%Y-%m-%d')}")
