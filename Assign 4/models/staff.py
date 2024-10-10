from datetime import datetime
from typing import List
from .customer import Customer
from .order import Order
from .item import PremadeBox, Vegetable
from .report import Report

class Person:
    """!
    Represents a person with basic attributes such as first name, last name, username, and password.
    """

    def __init__(self, first_name: str, last_name: str, username: str, password: str):
        """!
        Constructor for the Person class.
        Initializes the person's first name, last name, username, and password.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.__password = password  # Private attribute for password
class Staff(Person):
    """!
    Represents a staff member in the Fresh Harvest Veggies system.
    Inherits from the Person class and adds staff-specific attributes and methods.
    """

    def __init__(self, first_name: str, last_name: str, username: str, password: str, staff_id: int, date_joined: str, dept_name: str):
        """!
        Constructor for the Staff class.

        Initializes the staff member with a unique staff ID, department name, and the date they joined the company.

        @param first_name: The first name of the staff member.
        @param last_name: The last name of the staff member.
        @param username: The username for staff login.
        @param password: The password for staff login.
        @param staff_id: The unique identifier for the staff member.
        @param date_joined: The date when the staff joined the company.
        @param dept_name: The department name of the staff member.
        """
        super().__init__(first_name, last_name, username, password)  # Call base class constructor
        self.staff_id = staff_id  # Unique identifier for staff
        self.date_joined = datetime.strptime(date_joined, '%Y-%m-%d')  # Convert string date to datetime object
        self.dept_name = dept_name  # Department name
        self.list_of_customers: List[Customer] = []  # List to hold managed customers
        self.list_of_orders: List[Order] = []  # List to hold managed orders
        self.premade_boxes: List[PremadeBox] = []  # List of managed premade boxes
        self.veggies: List[Vegetable] = []  # List of managed vegetables

    def add_customer(self, customer: Customer) -> None:
        """!
        Adds a new customer to the staff's list of customers.
        
        @param customer: The Customer object to be added.
        """
        if customer not in self.list_of_customers:
            self.list_of_customers.append(customer)
            print(f"Customer '{customer.get_full_name()}' added to staff ID {self.staff_id}'s customer list.")
        else:
            print(f"Customer '{customer.get_full_name()}' is already in the list.")

    def remove_customer(self, customer_id: int) -> None:
        """!
        Removes a customer from the staff's list of customers based on their customer ID.
        
        @param customer_id: The unique ID of the customer to be removed.
        """
        self.list_of_customers = [cust for cust in self.list_of_customers if cust.cust_id != customer_id]
        print(f"Customer with ID {customer_id} removed from staff ID {self.staff_id}'s customer list.")

    def view_all_customers(self) -> str:
        """!
        Returns a string representation of all the customers managed by the staff member.

        @return: A formatted string containing the names and IDs of all customers.
        """
        if not self.list_of_customers:
            return "No customers managed by this staff member."
        customer_info = "\n".join([f"ID: {cust.cust_id}, Name: {cust.get_full_name()}" for cust in self.list_of_customers])
        return f"Customers managed by staff ID {self.staff_id}:\n{customer_info}"

    def add_order(self, order: Order) -> None:
        """!
        Adds a new order to the staff's list of managed orders.
        
        @param order: The Order object to be added.
        """
        self.list_of_orders.append(order)
        print(f"Order ID {order.get_order_id()} added to staff ID {self.staff_id}'s order list.")

    def update_order_status(self, order_id: int, status: str) -> None:
        """!
        Updates the status of an order managed by the staff member.
        
        @param order_id: The unique ID of the order to update.
        @param status: The new status of the order (e.g., 'Pending', 'Shipped', 'Delivered').
        """
        order = next((order for order in self.list_of_orders if order.get_order_id() == order_id), None)
        if order:
            order.set_order_status(status)
            print(f"Order ID {order_id} status updated to '{status}'.")
        else:
            print(f"Order ID {order_id} not found in staff ID {self.staff_id}'s order list.")

    def generate_report(self, report_type: str) -> str:
        """!
        Generates a report based on the specified type (e.g., 'sales', 'customers', 'items').

        @param report_type: The type of report to generate.
        @return: A string containing the report details.
        """
        report_data = {
            'sales': [{'date': '2023-10-01', 'amount': 200.0}, {'date': '2023-10-02', 'amount': 150.0}],
            'customers': [{'name': 'Alice', 'type': 'private'}, {'name': 'Bob Ltd.', 'type': 'corporate'}],
            'items': [{'name': 'Carrot', 'quantity_sold': 100}, {'name': 'Spinach', 'quantity_sold': 50}]
        }
        report = Report(report_data)
        if report_type == 'sales':
            return report.generate_sales_report("month")
        elif report_type == 'customers':
            return report.generate_customer_report()
        elif report_type == 'items':
            return report.generate_item_popularity_report()
        else:
            return f"Report type '{report_type}' is not recognized."
