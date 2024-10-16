# The main application file with routes

import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from models.customer import Customer  # Import your models
from models.order import Order, OrderLine
from models.payment import Payment, CreditCardPayment, DebitCardPayment
from models.item import Item, Veggie, PackVeggie, UnitPriceVeggie, PremadeBox
from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'mysql://root:1234@localhost:3306/fresh_harvest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# You can now use the models in your routes
@app.route('/')
def coverpage():
    return render_template('coverpage.html')

# # Other route definitions (e.g., for creating orders, viewing orders, etc.)
# @app.route('/create/', methods=['GET', 'POST'])
# def create():
#     if request.method == 'POST':
#         name = request.form['name']
#         price = float(request.form['price'])
#         new_item = Item(name=name, price=price)
#         db.session.add(new_item)
#         db.session.commit()
#         return redirect(url_for('index'))
#     return render_template('create.html')

if __name__ == '__main__':
    app.run(debug=True)
