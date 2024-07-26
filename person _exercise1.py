# Define the Person class
class Person:
    def __init__(self, firstname, lastname, height):
        # Initialise the firstname, lastname, and height attributes
        self.firstName = firstname
        self.lastName = lastname
        self.height = height

    def fullName(self):
        # Return the full name by combining firstName and lastName
        return self.firstName + " " + self.lastName

    def speak(self):
        # Return a greeting that includes the full name and height
        return "Hello, my name is " + self.fullName() + " and my height is: " + str(self.height)

# Create Person objects
person1 = Person("Jack", "Smith", 1.60)
person2 = Person("Mary", "Burt", 1.54)
person3 = Person("Sheila", "Barnes", 1.40)
person4 = Person("Ryan", "Green", 1.86)

# Print the full name of person1
print(person1.fullName())

# Task 1: Initialise an empty list named myStudents to store Person objects.

# Task 2: Display the length of myStudents to confirm that it is initially 0.

# Task 3: Add person1 and person2 to the myStudents list.

# Task 4: Print the length of myStudents after adding two objects to confirm it is 2.

# Task 5: Print the greeting messages for the Person objects at index 0 and 1 in the myStudents list.

# Task 6: Use the insert method to add person3 to the myStudents list at index 1.

# Task 7: Print the length of myStudents to confirm the total number of objects in the list after adding person3.

# Task 8: Print the greeting message of the Person object at index 1 to verify that person3 was correctly inserted at this position.

# Task 9: Use the pop method to remove the Person object at index 1 from the list.

# Task 10: Print the length of myStudents to verify the final number of objects in the list after the removal.
