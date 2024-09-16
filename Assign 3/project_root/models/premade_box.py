from typing import List
from .item import Item

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
        @param quantity: The number of premade boxes ordered.
        @param size: The size of the box, either 'small', 'medium', or 'large'.
        """
        super().__init__(name, price, quantity)
        self.size = size
        self.customItems = []

    def customizeBox(self, customItems: List[Item]) -> None:
        """!
        Customizes the contents of the premade box based on the available items.
        @param customItems: A list of Item objects to replace the default items in the box.
        """
        self.customItems = customItems

    def getBoxDetails(self) -> str:
        """!
        Returns the details of the premade box, including size and customized contents.
        @return A string describing the premade box's size and customized items.
        """
        details = f"Premade Box (Size: {self.size}, Quantity: {self.quantity})\n"
        if self.customItems:
            details += "Custom Items:\n"
            for item in self.customItems:
                details += f" - {item.name} (x{item.quantity})\n"
        else:
            details += "Default items are included.\n"
        return details
