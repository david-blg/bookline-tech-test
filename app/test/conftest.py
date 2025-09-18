import pytest
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from fastapi.testclient import TestClient
from app.main import app
from app.infra.db import JSONDatabase
import tempfile
import json

@pytest.fixture
def test_db():
    """
    Create a temporary database for tests.
    """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        test_data = {
            "cars": [
                {
                    "id": "test-car-1",
                    "brand": "Toyota",
                    "model": "Chaser",
                    "engine": "1JZ-GTE",
                    "version": "Tourer V",
                    "year": "1998",
                    "status": "available"
                },
                {
                    "id": "test-car-2", 
                    "brand": "Toyota",
                    "model": "Supra",
                    "engine": "2JZ-GTE",
                    "version": "MK4",
                    "year": "1996",
                    "status": "available"
                }
            ],
            "bookings": []
        }
        json.dump(test_data, f)
        temp_db_path = f.name
    
    test_db = JSONDatabase(json_path=temp_db_path)
    
    yield test_db
    
    import os
    os.unlink(temp_db_path)

@pytest.fixture
def client():
    """
    Test client for FastAPI.
    """
    return TestClient(app)

@pytest.fixture
def test_client():
    """
    Test client without mocking the database.
    """
    return TestClient(app)