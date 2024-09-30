from models import Customer, Order, OrderItem, Product, Payment

class Company:
    _instance = None

    def __new__(cls, *args, **kwargs):
        # Ensures the Company class follows the Singleton pattern (only one instance is created)
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, name):
        # Initializes the company with a name and lists for customers, products, orders, and payments
        self.companyName = name
        self.customers = []
        self.products = []
        self.orders = []
        self.payments = []

    # Create a new customer with a given name and balance, and add them to the customers list
    def create_customer(self, name, balance=0.0):
        customer = Customer(name, balance)
        self.customers.append(customer)
        return customer

    # Find a customer object by their name, return None if not found
    def find_customer(self, name):
        for customer in self.customers:
            if customer.customerName == name:
                return customer
        return None

    # Create a new product with a name and price, and add it to the products list
    def create_product(self, name, price):
        product = Product(name, price)
        self.products.append(product)
        return product

    # Find a product object by its name, return None if not found
    def find_product(self, name):
        for product in self.products:
            if product.productName == name:
                return product
        return None

    # Create a new order for a given customer and add it to the orders list and the customer's orders list
    def create_order(self, customer):
        order = Order(customer)
        self.orders.append(order)
        customer.add_order(order)
        return order

    # Add an order item to a given order by specifying the product name and quantity
    def add_order_item(self, order, product_name, quantity):
        product = self.find_product(product_name)
        if product is not None:
            order_item = OrderItem(product, quantity)
            order.add_item(order_item)
            subtotal = order.calculate_subtotal()
            return subtotal
        else:
            raise ValueError(f"Product '{product_name}' not found.")

    # Create a payment for a customer, adjust their balance, and add the payment to the payments list
    def create_payment(self, customer, amount):
        payment = Payment(customer, amount)
        self.payments.append(payment)
        customer.add_payment(payment)
        return payment

    # Get the list of all orders for a given customer
    def get_orders_for_customer(self, customer):
        return customer.orders

    # Get the list of all payments for a given customer
    def get_payments_for_customer(self, customer):
        return customer.payments

    # Get the list of all customers in the system
    def get_all_customers(self):
        return self.customers

    # Get the list of all orders placed by all customers
    def get_all_orders(self):
        return self.orders

    # Get the list of all payments made by all customers
    def get_all_payments(self):
        return self.payments

    # Submit an order and update the customer's balance by adding the order's total amount
    def submit_order(self, order):
        total = order.total()
        customer = order.customer
        customer.customerBalance += total
