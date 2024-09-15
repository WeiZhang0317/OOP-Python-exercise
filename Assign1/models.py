import datetime

class Customer:
    # Static variable to track the next customer ID
    next_id = 1000

    def __init__(self, name, balance=0.0):
        """
        Initializes a new Customer object with a unique ID, name, and balance.
        Also initializes empty lists for orders and payments.
        """
        self.customerID = Customer.next_id  # Assign a unique ID
        Customer.next_id += 1  # Increment the ID for the next customer
        self.customerName = name  # Customer's name
        self._customerBalance = balance  # Private balance attribute
        self.orders = []  # List to store customer orders
        self.payments = []  # List to store customer payments

    # Property to get the current balance
    @property
    def customerBalance(self):
        return self._customerBalance

    # Setter to update the customer's balance
    @customerBalance.setter
    def customerBalance(self, value):
        self._customerBalance = value
        
    # Add an order to the customer's list of orders
    def add_order(self, order):
        self.orders.append(order)

    # Add a payment to the customer's list of payments
    def add_payment(self, payment):
        self.payments.append(payment)

    # String representation of a customer, showing ID, name, and balance
    def __str__(self):
        return f"Customer {self.customerID}: {self.customerName}, Balance: {self.customerBalance}"


class Order:
    # Static variable to track the next order ID
    next_id = 10000

    def __init__(self, customer):
        """
        Initializes a new Order object with a unique ID, the current date,
        the customer placing the order, and an empty list for items.
        """
        self.orderID = Order.next_id  # Assign a unique ID
        Order.next_id += 1  # Increment the ID for the next order
        self.orderDate = datetime.date.today()  # Set the current date for the order
        self.customer = customer  # The customer who placed the order
        self.items = []  # List to store order items

    # Add an item to the order's list of items
    def add_item(self, item):
        self.items.append(item)
        
    # Calculate the subtotal of the order (sum of item prices * quantity)
    def calculate_subtotal(self):
        subtotal = sum(float(item.product.productPrice) * int(item.quantity) for item in self.items)
        return subtotal 

    # Calculate the total price of the order
    def total(self):
        return sum(item.total_price() for item in self.items)

    # String representation of the order showing the order ID, customer, and date
    def __str__(self):
        return f"Order {self.orderID} for Customer {self.customer.customerName} on {self.orderDate}"


class OrderItem:
    def __init__(self, product, quantity):
        """
        Initializes a new OrderItem object with a product and quantity.
        """
        self.product = product  # Product being ordered
        self.quantity = quantity  # Quantity of the product

    # Calculate the total price for this item (price * quantity)
    def total_price(self):
        return self.product.productPrice * self.quantity

    # String representation of the order item showing product name, quantity, and price
    def __str__(self):
        return f"{self.quantity} x {self.product.productName} @ {self.product.productPrice} each"


class Product:
    def __init__(self, name, price):
        """
        Initializes a new Product object with a name and price.
        """
        self.productName = name  # Product name
        self.productPrice = price  # Product price

    # String representation of the product showing name and price
    def __str__(self):
        return f"Product: {self.productName}, Price: {self.productPrice}"


class Payment:
    def __init__(self, customer, amount):
        """
        Initializes a new Payment object with a customer and payment amount.
        Also adjusts the customer's balance by adding the payment amount.
        """
        self.paymentAmount = amount  # Amount of the payment
        self.paymentDate = datetime.date.today()  # Set the payment date to today
        self.customer = customer  # The customer making the payment
        customer.customerBalance += amount  # Add the payment amount to the customer's balance

    # String representation of the payment showing the amount, customer, and date
    def __str__(self):
        return f"Payment of {self.paymentAmount} by Customer {self.customer.customerName} on {self.paymentDate}"
