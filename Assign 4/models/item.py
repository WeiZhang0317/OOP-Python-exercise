from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from db_config import Base

from typing import List

class Item(Base):  
    
    """!
    Represents an individual item that can be ordered by a customer.
    """
    
    __tablename__ = 'items' 

    id = Column(Integer, primary_key=True, autoincrement=True) 
    name = Column(String(50), nullable=False) 
    price = Column(Float, nullable=False)  
    
     # Relationship to the Inventory
    inventory = relationship("Inventory", back_populates="item", uselist=False)  # One-to-one relationship
    order_lines = relationship("OrderLine", back_populates="item")

    def __init__(self, name: str, price: float):
        """!
        Constructor for Item class.
        Initializes the name and price for the item.
        @param name: The name of the item (e.g., Carrot, Apple Pack).
        @param price: The price of the item.
        """
        self.name = name  # Public
        self.price = price # Public

    def get_price(self) -> float:
        """!
        Returns the price of the item.
        @return: The price as a float.
        """
        return self.price


    def set_price(self, new_price: float) -> None:
        """!
        Updates the price of the item.
        @param new_price: The new price to be set for the item.
        """
        self.price = new_price  # Encapsulation: price is modified through a method

    def calculate_total(self, quantity: int) -> float:
        """!
        Calculates the total cost for the item based on its price and quantity.
        @param quantity: The number of items being ordered.
        @return: A float representing the total cost for this item.
        """
        return self.get_price()* quantity  # Access private price attribute


class Veggie(Item):
    __tablename__ = 'veggie'

    id = Column(Integer, ForeignKey('items.id'), primary_key=True)  
    veg_name = Column(String(50), nullable=False)
 
    """!
    Represents a vegetable item that can be purchased individually or included in a premade box.
    """

    def __init__(self, name: str, price: float, veg_name: str):
        """!
        Constructor for Vegetable class.
        Initializes the vegetable's name, price, and veg_name.
        @param name: The name of the item.
        @param price: The price of the vegetable per unit.
        @param veg_name: The specific vegetable name (e.g., Carrot, Spinach).
        """
        super().__init__(name, price)  # Call base class constructor
        self.veg_name = veg_name  # Specific vegetable name


class WeightedVeggie(Veggie):
    """!
    Represents a vegetable that is priced based on weight.
    """
    __tablename__ = 'weighted_veggie'

    id = Column(Integer, ForeignKey('veggie.id'), primary_key=True)
    weight = Column(Float, nullable=False)  
    weight_per_kilo = Column(Float, nullable=False) 

    def __init__(self, name: str, price: float, veg_name: str, weight: float, weight_per_kilo: float):
        """!
        Constructor for WeightedVeggie class.
        Initializes the weighted vegetable with name, price, and weight attributes.
        @param name: The name of the item.
        @param price: The price of the item.
        @param veg_name: The specific vegetable name (e.g., Carrot).
        @param weight: The weight of the vegetable.
        @param weight_per_kilo: The price per kilo for this vegetable.
        """
        super().__init__(name, price, veg_name)
        self.weight = weight
        self.weight_per_kilo = weight_per_kilo

    def calculate_total_weight_price(self) -> float:
        """!
        Calculates the total price based on the weight and price per kilo.
        @return: The total price based on weight.
        """
        return self.weight * self.weight_per_kilo



class PackVeggie(Veggie):
    """!
    Represents a vegetable that is priced per pack.
    """
    __tablename__ = 'pack_veggie'

    id = Column(Integer, ForeignKey('veggie.id'), primary_key=True)
    num_of_pack = Column(Integer, nullable=False) 
    price_per_pack = Column(Float, nullable=False)  

    def __init__(self, name: str, price: float, veg_name: str, num_of_pack: int, price_per_pack: float):
        """!
        Constructor for PackVeggie class.
        Initializes the packed vegetable with name, price, and pack attributes.
        @param name: The name of the item.
        @param price: The price of the item.
        @param veg_name: The specific vegetable name.
        @param num_of_pack: The number of packs.
        @param price_per_pack: The price per pack.
        """
        super().__init__(name, price, veg_name)
        self.num_of_pack = num_of_pack
        self.price_per_pack = price_per_pack

    def calculate_total_pack_price(self) -> float:
        """!
        Calculates the total price based on the number of packs and price per pack.
        @return: The total price for all packs.
        """
        return self.num_of_pack * self.price_per_pack


class UnitPriceVeggie(Veggie):
    __tablename__ = 'unit_price_veggie'

    id = Column(Integer, ForeignKey('veggie.id'), primary_key=True)
    price_per_unit = Column(Float, nullable=False)  
    quantity = Column(Integer, nullable=False)  
    """!
    Represents a vegetable that is priced per unit.
    """

    def __init__(self, name: str, price: float, veg_name: str, price_per_unit: float, quantity: int):
        """!
        Constructor for UnitPriceVeggie class.
        Initializes the unit-priced vegetable with name, price, and quantity attributes.
        @param name: The name of the item.
        @param price: The price of the item.
        @param veg_name: The specific vegetable name.
        @param price_per_unit: The price per unit.
        @param quantity: The quantity of units.
        """
        super().__init__(name, price, veg_name)
        self.price_per_unit = price_per_unit
        self.quantity = quantity

    def calculate_total_unit_price(self) -> float:
        """!
        Calculates the total price based on the number of units and price per unit.
        @return: The total price for all units.
        """
        return self.quantity * self.price_per_unit


class PremadeBox(Item):
    """!
    Represents a premade box that can be customized with available vegetables.
    Inherits from Item.
    """
    __tablename__ = 'premade_boxes'

    id = Column(Integer, ForeignKey('items.id'), primary_key=True) 
    box_size = Column(String(20), nullable=False)  
    num_of_boxes = Column(Integer, nullable=False)  
    
    def __init__(self, name: str, price: float, box_size: str, num_of_boxes: int):
        """!
        Constructor for PremadeBox class.
        Initializes the premade box with name, price, box size, and number of boxes.
        @param name: The name of the premade box.
        @param price: The price of the premade box.
        @param box_size: The size of the box, either 'small', 'medium', or 'large'.
        @param num_of_boxes: The number of boxes.
        """
        super().__init__(name, price)
        self.box_size = box_size  # Public because it should be easily accessible
        self.num_of_boxes = num_of_boxes
        self.box_content: List[Veggie] = []  # Public for flexibility in customizing the box

    def add_content(self, veggie: List[Veggie]) -> None:
        """!
        Adds a list of vegetables to the box content.
        @param veggie: A list of Vegetable objects to include in the box.
        """
        self.box_content = veggie

    def get_box_details(self) -> str:
        """!
        Returns the details of the premade box, including size and contents.
        @return: A string describing the premade box's size and contents.
        """
        item_names = [item.veg_name for item in self.box_content]
        return f"Premade Box (Size: {self.box_size}) contains: {', '.join(item_names)}."

    def calculate_box_total(self) -> float:
        """!
        Calculates the total price for the entire box.
        @return: The total price of the box.
        """
        return self.get_price() * self.num_of_boxes

class Inventory(Base):
    """!
    Represents the inventory for items in the store.
    Each item will have a quantity indicating the available stock.
    """
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)  # ForeignKey to the Item table
    quantity = Column(Integer, nullable=False)  # Number of items available in stock

    # Relationship to the Item
    item = relationship("Item", back_populates="inventory")

    def __init__(self, item_id: int, quantity: int):
        """!
        Initializes the inventory for a specific item.
        @param item_id: The ID of the item in the inventory.
        @param quantity: The quantity of the item in stock.
        """
        self.item_id = item_id
        self.quantity = quantity

    def restock(self, additional_quantity: int):
        """!
        Adds stock to the current inventory.
        @param additional_quantity: The amount to add to the current stock.
        """
        self.quantity += additional_quantity

    def reduce_stock(self, quantity_sold: int):
        """!
        Reduces stock when an item is sold.
        @param quantity_sold: The quantity to reduce from stock.
        """
        if self.quantity >= quantity_sold:
            self.quantity -= quantity_sold
        else:
            raise ValueError("Not enough stock available")

    def __str__(self):
        """!
        String representation of the inventory item.
        """
        return f"Item ID: {self.item_id}, Quantity: {self.quantity}"