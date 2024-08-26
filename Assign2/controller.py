from models import Customer,Order, OrderItem, Product, Payment
class Company:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, name):
        self.companyName = name
        self.customers = []
        self.products = []
        self.orders = []
        self.payments = []

    # 创建客户
    def create_customer(self, name, balance=0.0):
        customer = Customer(name, balance)
        self.customers.append(customer)
        return customer

    # 查找客户
    def find_customer(self, name):
        for customer in self.customers:
            if customer.customerName == name:
                return customer
        return None

    # 创建产品
    def create_product(self, name, price):
        product = Product(name, price)
        self.products.append(product)
        return product

    # 查找产品
    def find_product(self, name):
        for product in self.products:
            if product.productName == name:
                return product
        return None

    # 为指定客户创建订单
    def create_order(self, customer):
        order = Order(customer)
        self.orders.append(order)
        customer.add_order(order)
        return order

    # 为指定订单添加订单项
    def add_order_item(self, order, product_name, quantity):
        product = self.find_product(product_name)
        if product is not None:
            order_item = OrderItem(product, quantity)
            order.add_item(order_item)
        else:
            raise ValueError(f"Product '{product_name}' not found.")

    # 为指定客户创建支付
    def create_payment(self, customer, amount):
        payment = Payment(customer, amount)
        self.payments.append(payment)
        customer.add_payment(payment)
        return payment

    # 获取指定客户的订单列表
    def get_orders_for_customer(self, customer):
        return customer.orders

    # 获取指定客户的支付列表
    def get_payments_for_customer(self, customer):
        return customer.payments

    # 获取所有客户
    def get_all_customers(self):
        return self.customers

    # 获取所有订单
    def get_all_orders(self):
        return self.orders

    # 获取所有支付
    def get_all_payments(self):
        return self.payments

    # 提交订单并更新客户余额
    def submit_order(self, order):
        total = order.total()
        customer = order.customer
        customer.customerBalance += total

