import os
from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from models.person import Person  # Import your Person model
from werkzeug.security import generate_password_hash, check_password_hash  # If you are using password hashing

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@localhost:3306/fresh_harvest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # For session management

db = SQLAlchemy(app)

# Home route
@app.route('/')
def coverpage():
    return render_template('coverpage.html')


# Sign-in Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Find the person in the database by username
        person = Person.query.filter_by(username=username).first()

        # Validate the password using the check_password method
        if person and person.check_password(password):
            session['user_id'] = person.id  # Store the user ID in session
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('login.html')


# Dashboard Route (to be created after login)
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('login'))

    # Fetch person details based on the session
    person = Person.query.get(session['user_id'])
    return render_template('dashboard.html', person=person)


# Logout Route
@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user ID from session
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
