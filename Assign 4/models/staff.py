from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models import db  # Import db instance from models/__init__.py
from datetime import datetime
from typing import List
from .customer import Customer  # Ensure correct import of Customer model
from .item import PremadeBox, Veggie  # Ensure correct import of PremadeBox and Veggie models
from .report import Report  # Ensure correct import of Report model
from .person import Person  # Ensure correct import of Person model


class Staff(Person):
    """Represents a staff member in the Fresh Harvest Veggies system, inheriting from Person."""
    __tablename__ = 'staff'

    id = Column(Integer, ForeignKey('persons.id'), primary_key=True)
    date_joined = Column(DateTime, default=datetime.now)
    dept_name = Column(String(50), nullable=False)

    # Relationships
    list_of_orders = relationship("Order", back_populates="staff")

    def __init__(self, first_name: str, last_name: str, username: str, password: str, dept_name: str):
        """Initialize a staff member with their department name and joining date."""
        super().__init__(first_name, last_name, username, password, role='staff') 
        self.dept_name = dept_name
        self.list_of_customers: List[Customer] = []
        self.list_of_orders = []
        self.premade_boxes: List[PremadeBox] = []
        self.veggie: List[Veggie] = []

    def add_customer(self, customer: Customer) -> None:
        """Add a new customer to the staff's managed customer list."""
        if customer not in self.list_of_customers:
            self.list_of_customers.append(customer)

    def remove_customer(self, customer_id: int) -> None:
        """Remove a customer from the staff's managed customer list by customer ID."""
        self.list_of_customers = [cust for cust in self.list_of_customers if cust.cust_id != customer_id]

    def view_all_customers(self) -> str:
        """Return a string representation of all customers managed by the staff member."""
        if not self.list_of_customers:
            return "No customers managed by this staff member."
        customer_info = "\n".join([f"ID: {cust.cust_id}, Name: {cust.get_full_name()}" for cust in self.list_of_customers])
        return f"Customers managed by staff ID {self.id}:\n{customer_info}"

    def add_order(self, order) -> None:
        """Add a new order to the staff's managed orders list."""
        self.list_of_orders.append(order)

    def update_order_status(self, order_id: int, status: str) -> None:
        """Update the status of a specific order managed by the staff."""
        order = next((order for order in self.list_of_orders if order.id == order_id), None)
        if order:
            order.set_order_status(status)

    def generate_report(self, report_type: str) -> str:
        """Generate a report based on the specified type (e.g., 'sales', 'customers', 'items')."""
        report = Report()  # Create a Report instance
        if report_type == 'sales':
            return report.generate_sales_report("month")
        elif report_type == 'customers':
            return report.generate_customer_report()
        elif report_type == 'items':
            return report.generate_item_popularity_report()
        else:
            return f"Report type '{report_type}' is not recognized."

    def __str__(self) -> str:
        """Return a string representation of the staff member, including their details."""
        return (f"Staff ID: {self.id}, Name: {self.get_full_name()}, Department: {self.dept_name}, "
                f"Date Joined: {self.date_joined.strftime('%Y-%m-%d')}, "
                f"Number of Managed Customers: {len(self.list_of_customers)}, "
                f"Number of Managed Orders: {len(self.list_of_orders)}")
