from fastapi.testclient import TestClient
from app.main import app
from datetime import date, timedelta

client = TestClient(app)

def test_get_all_cars_success():
    """
    Test to get all cars available.
    """
    response = client.get("/cars/")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "success"
    assert "data" in data
    assert "total_count" in data
    assert "message" in data
    
    assert isinstance(data["data"], list)
    assert data["total_count"] == len(data["data"])
    
    for car in data["data"]:
        assert car["status"] == "available"

def test_get_available_cars_for_valid_date():
    """
    Test getting available cars for a valid date.
    """
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    response = client.get(f"/cars/available?target_date={tomorrow}")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "success"
    assert isinstance(data["data"], list)
    assert "total_count" in data
    assert data["total_count"] == len(data["data"])

def test_get_available_cars_for_past_date():
    """
    Test getting available cars for a past date should fail.
    """
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    response = client.get(f"/cars/available?target_date={yesterday}")
    
    assert response.status_code == 400
    data = response.json()
    
    assert data["detail"]["status"] == "failed"
    assert data["detail"]["error_code"] == "INVALID_DATE_RANGE"
    assert "past dates" in data["detail"]["message"].lower()


def test_get_available_cars_for_today():
    """
    Test getting available cars for today.
    """
    today = date.today().isoformat()
    response = client.get(f"/cars/available?target_date={today}")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "success"
    assert isinstance(data["data"], list)


def test_cars_response_structure():
    """
    Test that car objects have expected structure.
    """
    response = client.get("/cars/")
    data = response.json()
    
    if data["data"]:
        car = data["data"][0]
        expected_fields = ["id", "brand", "model", "engine", "version", "year", "status"]
        
        for field in expected_fields:
            assert field in car
        
        assert car["status"] in ["available", "reserved", "maintenance"]