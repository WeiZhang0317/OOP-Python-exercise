# tests/test_db_config.py

import pytest
from sqlalchemy.exc import OperationalError
from db_config import engine, SessionLocal

def test_database_connection():
    """Test if the database engine connects successfully."""
    try:
        # Connect and immediately close to verify connection capability
        connection = engine.connect()
        connection.close()
    except OperationalError:
        pytest.fail("Database connection failed due to OperationalError.")

def test_session_creation():
    """Test if a session can be created and rolled back successfully."""
    session = SessionLocal()
    try:
        # Begin a session and rollback to ensure functionality
        session.begin()
        session.rollback()
        assert session.is_active is False, "Session should not be active after rollback."
    except Exception as e:
        pytest.fail(f"Session creation failed with error: {e}")
    finally:
        session.close()
