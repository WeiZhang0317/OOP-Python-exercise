# person.py
from sqlalchemy import Column, Integer, String
from db_config import Base
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # 这里初始化SQLAlchemy

class Person(db.Model):

    """!
    Represents a person with basic attributes such as first name, last name, username, and password.
    """
    __tablename__ = 'persons'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    __password = Column(String(255), nullable=False)

    def __init__(self, first_name: str, last_name: str, username: str, password: str):
        """!
        Constructor for the Person class.
        Initializes the person's first name, last name, username, and password.
        Password will be hashed before storing.
        @param first_name: The first name of the person.
        @param last_name: The last name of the person.
        @param username: The username of the person for login.
        @param password: The password of the person (it will be hashed before storing).
        """
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.set_password(password)  # Encrypts the password during initialization

    def get_full_name(self) -> str:
        """!
        Returns the full name of the person by concatenating the first and last name.
        @return: A string that contains the full name of the person.
        """
        return f"{self.first_name} {self.last_name}"

    def set_password(self, new_password: str) -> None:
        """!
        Sets a new password for the person and hashes it before storing.
        @param new_password: The new password to be hashed and stored.
        """
        self.__password = generate_password_hash(new_password)

    def check_password(self, password: str) -> bool:
        """!
        Checks if the provided password matches the hashed password stored.
        @param password: The plain-text password to check against the hashed password.
        @return: True if the password matches, otherwise False.
        """
        return check_password_hash(self.__password, password)

    def __str__(self) -> str:
        """!
        Returns a string representation of the person.
        @return: A string describing the person.
        """
        return f"Name: {self.get_full_name()}, Username: {self.username}"