from flask import Flask

from .order import order_blueprint
from .customer import customer_blueprint


def init_controller(app: Flask):
    app.register_blueprint(order_blueprint)
    app.register_blueprint(customer_blueprint)