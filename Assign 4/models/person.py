from sqlalchemy import Column, Integer, String
from werkzeug.security import check_password_hash
from models import db  # Import db instance from models package

class Person(db.Model):
    __tablename__ = 'persons'

    id = db.Column(Integer, primary_key=True, index=True)
    first_name = db.Column(String(50), nullable=False)
    last_name = db.Column(String(50), nullable=False)
    username = db.Column(String(50), unique=True, nullable=False)
    _Person__password = db.Column(String(255), nullable=False)  # Encrypted password
    role = db.Column(String(50), nullable=False)  # Role field

    def __init__(self, first_name: str, last_name: str, username: str, password: str, role: str):
        """Initializes the person with first name, last name, username, password, and role."""
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.__password = password  # Assumes password is already encrypted
        self.role = role  # Set the role

    def get_full_name(self) -> str:
        """Returns the full name by concatenating the first and last names."""
        return f"{self.first_name} {self.last_name}"

    def check_password(self, password: str) -> bool:
        """Verifies if the provided password matches the stored hashed password."""
        return check_password_hash(self._Person__password, password)

    def __str__(self) -> str:
        """Returns a string representation of the person, including name, username, and role."""
        return f"Name: {self.get_full_name()}, Username: {self.username}, Role: {self.role}"
