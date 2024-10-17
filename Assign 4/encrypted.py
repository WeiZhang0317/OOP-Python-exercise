# USE fresh_harvest12;
# ALTER TABLE persons MODIFY COLUMN `_Person__password` VARCHAR(255);


from flask import Flask
from werkzeug.security import generate_password_hash
from models.person import Person  # Assuming your Person model is already defined
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/fresh_harvest12'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Encrypt existing plaintext passwords
with app.app_context():  # Initialize the Flask application context to access the database
    persons = db.session.query(Person).all()  # Fetch all Person records

    for person in persons:
        # Check if the password is already hashed (Werkzeug hashes start with 'pbkdf2:sha256')
        if not person._Person__password.startswith('pbkdf2:sha256'):
            # Encrypt the plain-text password
            hashed_password = generate_password_hash(person._Person__password)
            person._Person__password = hashed_password

    # Commit the changes to the database
    db.session.commit()

print("Passwords encrypted successfully!")
