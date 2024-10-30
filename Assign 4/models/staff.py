from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models import db  # Import db instance from models/__init__.py
from datetime import datetime
from typing import List
from .customer import Customer  # Ensure correct import of Customer model
from .item import PremadeBox, Veggie  # Ensure correct import of PremadeBox and Veggie models
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


    def __str__(self) -> str:
        """Return a string representation of the staff member, including their details."""
        return (f"Staff ID: {self.id}, Name: {self.get_full_name()}, Department: {self.dept_name}, "
                f"Date Joined: {self.date_joined.strftime('%Y-%m-%d')}, "
                f"Number of Managed Customers: {len(self.list_of_customers)}, "
                f"Number of Managed Orders: {len(self.list_of_orders)}")
