import datetime

class Customer:
    next_id = 1000

    def __init__(self, name, balance=0.0):
        self.customerID = Customer.next_id
        Customer.next_id += 1
        self.customerName = name
        self._customerBalance = balance  
        self.orders = []
        self.payments = []

    @property
    def customerBalance(self):
        return self._customerBalance

    @customerBalance.setter
    def customerBalance(self, value):
        self._customerBalance = value
        
    def add_order(self, order):
        self.orders.append(order)

    def add_payment(self, payment):
        self.payments.append(payment)

    def __str__(self):
        return f"Customer {self.customerID}: {self.customerName}, Balance: {self.customerBalance}"


class Order:
    next_id = 10000

    def __init__(self, customer):
        self.orderID = Order.next_id
        Order.next_id += 1
        self.orderDate = datetime.date.today()
        self.customer = customer
        self.items = []

    def add_item(self, item):
        self.items.append(item)
        
    def calculate_subtotal(self):
        subtotal = sum(item.product.productPrice * item.quantity for item in self.items)
        return subtotal    

    def total(self):
        return sum(item.total_price() for item in self.items)

    def __str__(self):
        return f"Order {self.orderID} for Customer {self.customer.customerName} on {self.orderDate}"


class OrderItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def total_price(self):
        return self.product.productPrice * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.productName} @ {self.product.productPrice} each"

class Product:
    def __init__(self, name, price):
        self.productName = name
        self.productPrice = price

    def __str__(self):
        return f"Product: {self.productName}, Price: {self.productPrice}"

class Payment:
    def __init__(self, customer, amount):
        self.paymentAmount = amount
        self.paymentDate = datetime.date.today()
        self.customer = customer
        customer.customerBalance -= amount

    def __str__(self):
        return f"Payment of {self.paymentAmount} by Customer {self.customer.customerName} on {self.paymentDate}"
