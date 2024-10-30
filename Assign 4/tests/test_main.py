# tests/test_main.py

import pytest
from db_config import engine
from sqlalchemy.exc import OperationalError
from models import db
from app import app

def test_table_creation_with_app_context():
    """Test if tables are created within the app context in main.py."""
    with app.app_context():
        try:
            db.create_all()  # Create tables
            # Check if a specific table exists, such as 'customers'
            assert 'customers' in db.metadata.tables
            assert 'orders' in db.metadata.tables
            assert 'items' in db.metadata.tables
            assert 'staff' in db.metadata.tables
        except OperationalError as e:
            pytest.fail(f"Table creation failed due to database error: {str(e)}")
        except Exception as e:
            pytest.fail(f"Unexpected error during table creation: {str(e)}")

def test_main_script_execution(capfd):
    """Test if the main.py script prints the expected output when run."""
    from main import app, db  # Import main to capture its output

    with app.app_context():
        db.create_all()
        
    out, err = capfd.readouterr()  # Capture stdout and stderr
    assert "Database tables created!" in out, "Expected output was not printed."
