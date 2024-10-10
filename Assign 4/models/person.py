# person.py

class Person:
    """!
    Represents a person with basic attributes such as first name, last name, username, and password.
    """

    def __init__(self, first_name: str, last_name: str, username: str, password: str):
        """!
        Constructor for the Person class.
        Initializes the person's first name, last name, username, and password.
        @param first_name: The first name of the person.
        @param last_name: The last name of the person.
        @param username: The username of the person for login.
        @param password: The password of the person.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.__password = password  # Private attribute for storing password

    def get_full_name(self) -> str:
        """!
        Returns the full name of the person by concatenating the first and last name.
        @return: A string that contains the full name of the person.
        """
        return f"{self.first_name} {self.last_name}"

    def set_password(self, new_password: str) -> None:
        """!
        Sets a new password for the person.
        @param new_password: The new password to be set.
        @raise ValueError: If the new password does not meet the required criteria.
        """
        if self.__validate_password(new_password):
            self.__password = new_password
        else:
            raise ValueError("Password must contain at least 8 characters, including one uppercase, one lowercase, and one number.")

    def check_password(self, password: str) -> bool:
        """!
        Checks if the provided password matches the stored password.
        @param password: The password to check against the stored password.
        @return: True if the password matches, otherwise False.
        """
        return self.__password == password

    def __validate_password(self, password: str) -> bool:
        """!
        Validates if the password meets the required criteria.
        @param password: The password to validate.
        @return: True if the password is valid, otherwise False.
        """
        if len(password) < 8:
            return False
        has_upper = any(char.isupper() for char in password)
        has_lower = any(char.islower() for char in password)
        has_digit = any(char.isdigit() for char in password)
        return has_upper and has_lower and has_digit

    def __str__(self) -> str:
        """!
        Returns a string representation of the person.
        @return: A string describing the person.
        """
        return f"Name: {self.get_full_name()}, Username: {self.username}"
