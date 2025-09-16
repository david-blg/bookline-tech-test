from fastapi.testclient import TestClient
from app.main import app
from datetime import date, timedelta

client = TestClient(app)

def test_get_all_cars():
    """
    Test to get all cars.
    """
    response = client.get("/cars/")
    
    assert response.status_code == 200
    assert "data" in response.json()
    assert isinstance(response.json()["data"], list)
    print("✓ test_get_all_cars passed")

def test_get_available_cars_for_date():
    """
    Test to get available cars for a specific date.
    """
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    response = client.get(f"/cars/available?target_date={tomorrow}")
    
    assert response.status_code == 200
    assert "data" in response.json()
    assert isinstance(response.json()["data"], list)
    print("✓ test_get_available_cars_for_date passed")