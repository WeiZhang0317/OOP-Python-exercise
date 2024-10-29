# python -m pytest -v tests/test_item_model.py

import pytest
from models import db
from models.item import Item, Veggie, WeightedVeggie, PackVeggie, UnitPriceVeggie, PremadeBox, Inventory
from app import app

@pytest.fixture
def setup_db():
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

def test_item_initialization(setup_db):
    """Test basic initialization of Item."""
    item = Item(name="Carrot", price=1.5)
    assert item.name == "Carrot"
    assert item.price == 1.5

def test_item_price_methods(setup_db):
    """Test Item price getter and setter."""
    item = Item(name="Apple", price=2.0)
    item.set_price(2.5)
    assert item.get_price() == 2.5

def test_item_calculate_total(setup_db):
    """Test calculate_total method for Item."""
    item = Item(name="Banana", price=1.2)
    total = item.calculate_total(quantity=5)
    assert total == 6.0  # 1.2 * 5

def test_weighted_veggie_initialization(setup_db):
    """Test initialization of WeightedVeggie with price per kilogram."""
    weighted_veggie = WeightedVeggie(name="Tomato", price=0, veg_name="Tomato", weight_per_kilo=3.0, unit_type="kg")
    assert weighted_veggie.get_weight_price() == "3.0 per kg"
    assert weighted_veggie.calculate_total(2) == 6.0  # 3.0 * 2 kg

def test_pack_veggie_initialization(setup_db):
    """Test initialization and calculate_total of PackVeggie."""
    pack_veggie = PackVeggie(name="Bell Pepper", price=5.0, veg_name="Bell Pepper Pack", num_in_pack=3)
    total = pack_veggie.calculate_total(quantity=2)
    assert total == 10.0  # 5.0 * 2 packs

def test_unit_price_veggie_initialization(setup_db):
    """Test UnitPriceVeggie initialization and unit pricing."""
    unit_price_veggie = UnitPriceVeggie(name="Cucumber", price=0, veg_name="Cucumber", price_per_unit=0.75, unit_type="piece")
    assert unit_price_veggie.get_unit_price() == "0.75 per piece"
    assert unit_price_veggie.calculate_total(4) == 3.0  # 0.75 * 4 pieces

def test_premade_box_initialization(setup_db):
    """Test PremadeBox initialization and max content check."""
    premade_box = PremadeBox(name="Veggie Box", price=15.0, box_size="small")
    assert premade_box.max_content == 3

def test_premade_box_add_items(setup_db):
    """Test adding items to a PremadeBox and ensure max content validation."""
    premade_box = PremadeBox(name="Veggie Box", price=15.0, box_size="small")
    veggie = Veggie(name="Spinach", price=1.5, veg_name="Spinach")

    # Add items within max content limit
    premade_box.add_items_to_box(veggie, 2)
    assert len(premade_box.box_content) == 2

    # Exceed max content should raise ValueError
    with pytest.raises(ValueError):
        premade_box.add_items_to_box(veggie, 2)  # Adding 2 exceeds max content of 3

def test_inventory_operations(setup_db):
    """Test inventory restock, reduce, and check stock functionality."""
    inventory = Inventory(item_id=1, quantity=10)

    # Restock and verify quantity
    inventory.restock(5)
    assert inventory.quantity == 15

    # Reduce stock and verify
    inventory.reduce_stock(5)
    assert inventory.quantity == 10

    # Test stock checking
    assert inventory.check_stock(8) is True
    assert inventory.check_stock(12) is False

    # Test reducing stock below available quantity raises ValueError
    with pytest.raises(ValueError):
        inventory.reduce_stock(20)
