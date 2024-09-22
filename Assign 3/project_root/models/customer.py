from typing import List
from .order import Order

class Customer:
    """!
    Represents a customer in the Fresh Harvest Veggies system.
    """

    def __init__(self, firstName: str, lastName: str, balance: float, address: str):
        """!
        Constructor for Customer class.
        @param firstName: The customer's first name.
        @param lastName: The customer's last name.
        @param balance: The customer's current balance.
        @param address: The customer's delivery address.
        """
        pass

    def fullName(self) -> str:
        """!
        The method fullName returns the full name of the customer
        by concatenating the first and last name.
        @return A string that contains the full name of the customer.
        """
        pass

    def placeOrder(self, order: Order) -> None:
        """!
        Places a new order for the customer.
        @param order: The Order object to be placed by the customer.
        """
        pass

    def viewOrderHistory(self) -> List[Order]:
        """!
        Returns the order history of the customer.
        @return A list of Order objects representing the customer's order history.
        """
        pass

    def viewBalance(self) -> float:
        """!
        Returns the customer's balance.
        @return: The balance as a float.
        """
        pass




class PrivateCustomer(Customer):
    """!
    Represents a private customer. Inherits from Customer.
    """

    def __init__(self, firstName: str, lastName: str, balance: float, address: str):
        """!
        Constructor for PrivateCustomer class.
        @param firstName: The private customer's first name.
        @param lastName: The private customer's last name.
        @param balance: The private customer's current balance.
        @param address: The private customer's delivery address.
        """
        pass

    def canPlaceOrder(self) -> bool:
        """!
        Checks if the private customer can place an order.
        Private customers cannot place orders if their balance exceeds $100.
        @return True if the balance is <= $100, otherwise False.
        """
        pass


class CorporateCustomer(Customer):
    """!
    Represents a corporate customer. Inherits from Customer.
    """

    def __init__(self, firstName: str, lastName: str, balance: float, address: str, creditLimit: float):
        """!
        Constructor for CorporateCustomer class.
        @param firstName: The corporate customer's first name.
        @param lastName: The corporate customer's last name.
        @param balance: The corporate customer's current balance.
        @param address: The corporate customer's delivery address.
        @param creditLimit: The corporate customer's credit limit.
        """
        pass

    def canPlaceOrder(self) -> bool:
        """!
        Checks if the corporate customer can place an order.
        Corporate customers cannot place orders if their balance is less than their credit limit.
        @return True if the balance is >= credit limit, otherwise False.
        """
        pass

    def getDiscount(self) -> float:
        """!
        Returns the discount for corporate customers.
        Corporate customers get a 10% discount for each order.
        @return A float representing the 10% discount.
        """
        pass
