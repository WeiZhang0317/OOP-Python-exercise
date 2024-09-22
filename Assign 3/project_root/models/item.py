from typing import List

class Item:
    """!
    Represents an individual item that can be ordered by a customer.
    """

    def __init__(self, name: str, price: float, quantity: int, category: str, unit_type: str) -> None:
        """!
        Constructor for Item class.
        @param name: The name of the item (e.g., Carrot, Apple Pack).
        @param price: The price of the item per unit, weight, or pack.
        @param quantity: The quantity of the item being ordered (units, weight, or packs).
        @param category: The category of the vegetable (e.g., leafy greens, root vegetables).
        @param unit_type: The unit type for ordering (e.g., bunch, weight, punnet, pack).
        """
        pass

    def calculateItemTotal(self) -> float:
        """!
        Calculates the total cost for the item based on its price and quantity.
        @return: A float representing the total cost for this item.
        """
        pass



class Vegetable(Item):
    """!
    Represents a vegetable item that can be purchased individually or included in a premade box.
    """

    def __init__(self, name: str, price: float, available_quantity: int) -> None:
        """!
        Constructor for Vegetable class.
        @param name: The name of the vegetable.
        @param price: The price of the vegetable per unit.
        @param available_quantity: The quantity of the vegetable available for purchase.
        """
        pass


    def purchase(self, quantity: int) -> None:
        """!
        Allows purchasing a specified quantity of the vegetable.
        @param quantity: The quantity of the vegetable to purchase.
        """
        pass



class PremadeBox(Item):
    """!
    Represents a premade box that can be customized with available vegetables.
    Inherits from Item.
    """

    def __init__(self, name: str, price: float, quantity: int, size: str) -> None:
        """!
        Constructor for PremadeBox class.
        @param name: The name of the premade box.
        @param price: The price of the premade box.
        @param quantity: The number of boxes.
        @param size: The size of the box, either 'small', 'medium', or 'large'.
        """
        pass


    def customizeBox(self, customItems: List[Vegetable]) -> None:
        """!
        Customizes the contents of the premade box based on the availability of vegetables.
        @param customItems: A list of Vegetable objects to replace the default items in the box.
        """
        pass


    def getBoxDetails(self) -> str:
        """!
        Returns the details of the premade box, including size and customized contents.
        @return: A string describing the premade box's size and customized items.
        """
        pass
