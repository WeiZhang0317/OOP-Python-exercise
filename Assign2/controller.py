from models import Customer,Order, OrderItem, Product, Payment
class Company:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


    def __init__(self, name):
        self.companyName = name
        self.customers = []
        self.products = []
        self.orders = []
        self.payments = []

    # Create customers.  
    def create_customer(self, name, balance=0.0):
        customer = Customer(name, balance)
        self.customers.append(customer)
        return customer

    # Find a customer object based on customer’s name
    def find_customer(self, name):
        for customer in self.customers:
            if customer.customerName == name:
                return customer
        return None

    # Create products.  
    def create_product(self, name, price):
        product = Product(name, price)
        self.products.append(product)
        return product

    # Find products
    def find_product(self, name):
        for product in self.products:
            if product.productName == name:
                return product
        return None

    # Add an order for a given customer.
    def create_order(self, customer):
        order = Order(customer)
        self.orders.append(order)
        customer.add_order(order)
        return order

    # Add an order item for a given order.  
    def add_order_item(self, order, product_name, quantity):
        product = self.find_product(product_name)
        if product is not None:
            order_item = OrderItem(product, quantity)
            order.add_item(order_item)
            subtotal = order.calculate_subtotal()
            return subtotal
        else:
            raise ValueError(f"Product '{product_name}' not found.")

    # Add a payment for a given customer.
    def create_payment(self, customer, amount):
        payment = Payment(customer, amount)
        self.payments.append(payment)
        customer.add_payment(payment)
        return payment

    # Provide the list of orders for a given customer. 
    def get_orders_for_customer(self, customer):
        return customer.orders

    # Provide the list of payments for a given customer. 
    def get_payments_for_customer(self, customer):
        return customer.payments

    # Provide a list of all customers. 
    def get_all_customers(self):
        return self.customers

    # Provide a list of all orders. 
    def get_all_orders(self):
        return self.orders

    # Provide a list of all payments.
    def get_all_payments(self):
        return self.payments

    # Submit order and update customer balance
    def submit_order(self, order):
        total = order.total()
        customer = order.customer
        customer.customerBalance += total

