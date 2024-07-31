# Define the Person class
class Person:
    def __init__(self, fname, lname, height):
        # Initialise the attributes of the Person class
        self.firstName = fname
        self.lastName = lname
        self.height = height

    def personInfo(self):
        # Return a string containing the person's full name and height
        return self.firstName + " " + self.lastName + " " + str(self.height)

# Initialise two empty lists
list1 = []
list2 = []

# Create Person objects
person1 = Person("Alice", "Johnson", 1.65)
person2 = Person("Bob", "Williams", 1.70)
person3 = Person("Cathy", "Brown", 1.55)
person4 = Person("David", "Davis", 1.80)
person5 = Person("Eve", "Miller", 1.75)
person6 = Person("Frank", "Wilson", 1.68)

#change value of height
person6.height = 5.00

# Add Person objects to list1
list1.append(person1)
list1.append(person2)
list1.append(person3)
list1.append(person5)

# Add Person objects to list2
list2.append(person3)
list2.append(person4)
list2.append(person5)
list2.append(person6)

# Task 1: Print the full info of all Person objects that are in BOTH lists
for person1 in list1:
    for person2 in list2:
        if person1 == person2:
            print(person1.personInfo())