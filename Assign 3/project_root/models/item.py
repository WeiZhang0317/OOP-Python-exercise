from typing import List

class Item:
    """!
    Represents an individual item that can be ordered by a customer.
    """

    def __init__(self, name: str, price: float, quantity: int, category: str, unit_type: str) -> None:
        """!
        Constructor for Item class.
        Initializes the name, price, quantity, category, and unit type for the item.
        @param name: The name of the item (e.g., Carrot, Apple Pack).
        @param price: The price of the item per unit, weight, or pack.
        @param quantity: The quantity of the item being ordered (units, weight, or packs).
        @param category: The category of the vegetable (e.g., leafy greens, root vegetables).
        @param unit_type: The unit type for ordering (e.g., bunch, weight, punnet, pack).
        """
        self.name = name  # Public
        self.__price = price  # Private because it can be modified only internally
        self.quantity = quantity  # Public
        self.category = category  # Public
        self.unit_type = unit_type  # Public

    def calculateItemTotal(self) -> float:
        """!
        Calculates the total cost for the item based on its price and quantity.
        @return: A float representing the total cost for this item.
        """
        return self.__price * self.quantity  # Access private price attribute

    def getPrice(self) -> float:
        """!
        Returns the price of the item.
        @return: The price as a float.
        """
        return self.__price

    def setPrice(self, newPrice: float) -> None:
        """!
        Updates the price of the item.
        @param newPrice: The new price to be set for the item.
        """
        self.__price = newPrice  # Encapsulation: price is modified through a method


class Vegetable(Item):
    """!
    Represents a vegetable item that can be purchased individually or included in a premade box.
    """

    def __init__(self, name: str, price: float, available_quantity: int) -> None:
        """!
        Constructor for Vegetable class.
        Initializes the vegetable's name, price, and available quantity.
        @param name: The name of the vegetable.
        @param price: The price of the vegetable per unit.
        @param available_quantity: The quantity of the vegetable available for purchase.
        """
        super().__init__(name, price, available_quantity, category="vegetable", unit_type="unit")  # Inherits from Item
        self.__available_quantity = available_quantity  # Private because it's an internal control attribute

    def purchase(self, quantity: int) -> None:
        """!
        Allows purchasing a specified quantity of the vegetable.
        Updates the available quantity after purchase.
        @param quantity: The quantity of the vegetable to purchase.
        """
        if quantity <= self.__available_quantity:
            self.__available_quantity -= quantity
            print(f"Purchased {quantity} units of {self.name}.")
        else:
            print(f"Not enough {self.name} in stock.")

    def getAvailableQuantity(self) -> int:
        """!
        Returns the available quantity of the vegetable.
        @return: The available quantity as an integer.
        """
        return self.__available_quantity


class PremadeBox(Item):
    """!
    Represents a premade box that can be customized with available vegetables.
    Inherits from Item.
    """

    def __init__(self, name: str, price: float, quantity: int, size: str) -> None:
        """!
        Constructor for PremadeBox class.
        Initializes the premade box with a name, price, quantity, and size.
        @param name: The name of the premade box.
        @param price: The price of the premade box.
        @param quantity: The number of boxes.
        @param size: The size of the box, either 'small', 'medium', or 'large'.
        """
        super().__init__(name, price, quantity, category="box", unit_type="box")
        self.size = size  # Public because it should be easily accessible
        self.customItems: List[Vegetable] = []  # Public for flexibility in customizing the box

    def customizeBox(self, customItems: List[Vegetable]) -> None:
        """!
        Customizes the contents of the premade box based on the availability of vegetables.
        Replaces default items with the provided customItems.
        @param customItems: A list of Vegetable objects to replace the default items in the box.
        """
        self.customItems = customItems  # Replace the default items with custom vegetables
        print(f"Customized the box with {len(customItems)} vegetables.")

    def getBoxDetails(self) -> str:
        """!
        Returns the details of the premade box, including size and customized contents.
        @return: A string describing the premade box's size and customized items.
        """
        itemNames = [item.name for item in self.customItems]
        return f"Premade Box (Size: {self.size}) contains: {', '.join(itemNames)}."
