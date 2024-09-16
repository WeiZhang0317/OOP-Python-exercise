class Item:
    """!
    Represents an individual item that can be ordered by a customer.
    """

    def __init__(self, name: str, price: float, quantity: int):
        """!
        Constructor for Item class.
        @param name: The name of the item (e.g., Carrot, Apple Pack).
        @param price: The price of the item per unit, weight, or pack.
        @param quantity: The quantity of the item being ordered (units, weight, or packs).
        """
        pass

    def calculateItemTotal(self) -> float:
        """!
        Calculates the total cost for the item based on its price and quantity.
        @return A float representing the total cost for this item.
        """
        pass


class PremadeBox(Item):
    """!
    Represents a premade box that can be customized with available vegetables.
    Inherits from Item.
    """

    def __init__(self, name: str, price: float, quantity: int, size: str):
        """!
        Constructor for PremadeBox class.
        @param name: The name of the premade box.
        @param price: The price of the premade box.
        @param quantity: The number of boxes.
        @param size: The size of the box, either 'small', 'medium', or 'large'.
        """
        pass

    def customizeBox(self, customItems: list) -> None:
        """!
        Customizes the contents of the premade box based on the availability of vegetables.
        @param customItems: A list of Item objects that will replace the default items in the box.
        """
        pass
