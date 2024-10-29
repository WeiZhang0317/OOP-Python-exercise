from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from models import db

from typing import List


class Item(db.Model):
    
    """!
    Represents an individual item that can be ordered by a customer.
    """
    
    __tablename__ = 'items' 

    id = Column(Integer, primary_key=True, autoincrement=True) 
    name = Column(String(50), nullable=False) 
    price = Column(Float, nullable=False)  
    type = Column(String(50))  
    __mapper_args__ = {
        'polymorphic_on': type,  
        'polymorphic_identity': 'item'
    }
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
        return self.get_price() * quantity  # Access private price attribute


class Veggie(Item):
    __tablename__ = 'veggie'

    id = Column(Integer, ForeignKey('items.id'), primary_key=True)  
    veg_name = Column(String(50), nullable=False)
    __mapper_args__ = {
    'polymorphic_identity': 'veggie'  
}

 
    """!
    Represents a vegetable item that can be purchased individually.
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
    weight_per_kilo = Column(Float, nullable=False)  # Price per kilogram or other weight unit
    unit_type = Column(String(20), nullable=False)  # Unit type (e.g., 'kg', 'g')

    __mapper_args__ = {
        'polymorphic_identity': 'weighted_veggie'
    }

    def __init__(self, name: str, price: float, veg_name: str, weight_per_kilo: float, unit_type: str):
        """!
        Constructor for WeightedVeggie class.
        Initializes the weighted vegetable with name, price per kilo, and unit type.
        @param name: The name of the item.
        @param price: The base price of the item.
        @param veg_name: The specific vegetable name (e.g., Carrot).
        @param weight_per_kilo: The price per kilo for this vegetable.
        @param unit_type: The unit of measurement (e.g., 'kg', 'g').
        """
        super().__init__(name, price, veg_name)
        self.weight_per_kilo = weight_per_kilo
        self.unit_type = unit_type  # Set the measurement unit (e.g., 'kg', 'g')

    def get_weight_price(self) -> str:
        """!
        Returns a string with the unit type and price per weight unit.
        @return: A string displaying price per unit and weight unit (e.g., '3.0 per kg').
        """
        return f"{self.weight_per_kilo} per {self.unit_type}"
    
    def calculate_total(self, quantity: float) -> float:
        """!
        Calculates the total price based on the weight (treated as quantity) chosen by the customer.
        @param quantity: The amount of weight (e.g., 2 kg).
        @return: The total price.
        """
        return self.weight_per_kilo * quantity
    

class PackVeggie(Veggie):
    """!
    Represents a vegetable that is priced per pack.
    """
    __tablename__ = 'pack_veggie'

    id = Column(Integer, ForeignKey('veggie.id'), primary_key=True)
    num_of_pack = Column(Integer, nullable=False) 


    __mapper_args__ = {
        'polymorphic_identity': 'pack_veggie'
    } 

    def __init__(self, name: str, price: float, veg_name: str, num_in_pack: int):
        """!
        Constructor for PackVeggie class.
        Initializes the packed vegetable with name, price, and pack attributes.
        @param name: The name of the item.
        @param price: The price of the item.
        @param veg_name: The specific vegetable name.
        @param num_of_pack: The number in packs.
        @param price_per_pack: The price per pack.
        """
        super().__init__(name, price, veg_name)
        self.num_of_pack = num_in_pack
        
    def calculate_total(self, quantity: int) -> float:
        """!
        Calculates the total price based on the number of packs chosen by the customer.
        @param quantity: The number of packs (e.g., 3 packs).
        @return: The total price.
        """
        return self.price * quantity


class UnitPriceVeggie(Veggie):
    __tablename__ = 'unit_price_veggie'

    id = Column(Integer, ForeignKey('veggie.id'), primary_key=True)
    price_per_unit = Column(Float, nullable=False)  # Price per unit (e.g., price per piece, per bunch)
    unit_type = Column(String(20), nullable=False)  # Unit type (e.g., 'piece', 'bunch', 'bundle')

    __mapper_args__ = {
        'polymorphic_identity': 'unit_price_veggie'
    }

    """!
    Represents a vegetable that is priced per unit (e.g., 'piece', 'bunch').
    """


    def __init__(self, name: str, price: float, veg_name: str, price_per_unit: float, unit_type: str):
        """!
        Constructor for UnitPriceVeggie class.
        Initializes the unit-priced vegetable with name, price, and unit type.
        @param name: The name of the item.
        @param price: The price of the item.
        @param veg_name: The specific vegetable name.
        @param price_per_unit: The price per unit.
        @param unit_type: The type of unit (e.g., 'piece', 'bunch').
        """
        super().__init__(name, price, veg_name)
        self.price_per_unit = price_per_unit
        self.unit_type = unit_type  # Set the measurement unit (e.g., 'piece', 'bunch')

    def get_unit_price(self) -> str:
        """!
        Returns a string with the unit type and price.
        @return: A string displaying price per unit and unit type.
        """
        return f"{self.price_per_unit} per {self.unit_type}"
    
    
    def calculate_total(self, quantity: int) -> float:
        """!
        Calculates the total price based on the quantity chosen by the customer.
        @param quantity: The number of units (e.g., 5 pieces).
        @return: The total price.
        """
        return self.price_per_unit * quantity


class PremadeBox(Item):
    """Represents a premade box that can be customized with available vegetables."""
    
    __tablename__ = 'premade_boxes'

    id = Column(Integer, ForeignKey('items.id'), primary_key=True)
    box_size = Column(String(20), nullable=False)
    max_content = Column(Integer, nullable=False)  # Maximum number of veggies allowed in the box

    __mapper_args__ = {
        'polymorphic_identity': 'premade_box'
    }

    def __init__(self, name: str, price: float, box_size: str):
        super().__init__(name, price)
        self.box_size = box_size
        self.box_content: List[Veggie] = []

        # Set the maximum content based on the box size
        if box_size == 'small':
            self.max_content = 3
        elif box_size == 'medium':
            self.max_content = 6
        elif box_size == 'large':
            self.max_content = 9

    def add_items_to_box(self, veggie: Item, quantity: int) -> None:
        """Adds the vegetable to the box if the box is not full."""
        if len(self.box_content) + quantity > self.max_content:
            raise ValueError(f"The {self.box_size} box can only contain {self.max_content} items.")
        
        self.box_content.extend([veggie] * quantity)  # Add the vegetable multiple times based on quantity


    def get_box_details(self) -> str:
        """Returns the details of the premade box, including size and contents."""
        item_names = [item.veg_name for item in self.box_content]
        return f"Premade Box (Size: {self.box_size}) contains: {', '.join(item_names)}."

    def calculate_box_total(self) -> float:
        """Calculates the total price for the premade box."""
        if self.box_size == 'small':
            return 15.0
        elif self.box_size == 'medium':
            return 20.0
        elif self.box_size == 'large':
            return 30.0




class Inventory(db.Model): 
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
        
    def check_stock(self, quantity_requested: int) -> bool:
        """!
        Checks if there is enough stock to fulfill a request.
        @param quantity_requested: The quantity to check.
        @return: True if enough stock is available, otherwise False.
        """
        return self.quantity >= quantity_requested    

    def __str__(self):
        """!
        String representation of the inventory item.
        """
        return f"Item ID: {self.item_id}, Quantity: {self.quantity}"