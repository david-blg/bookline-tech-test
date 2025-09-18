from uuid import uuid4
from fastapi.testclient import TestClient
from app.main import app
import pytest
from datetime import date, timedelta

client = TestClient(app)


def test_get_all_bookings():
    """Test getting all bookings."""
    response = client.get("/bookings/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["data"], list)
    assert "total_count" in data


def test_create_booking_success():
    """Test creating a new booking."""

    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    car_response = client.get(f"/cars/available?target_date={tomorrow}")
    available_cars = car_response.json()["data"]

    if not available_cars:
        pytest.skip("No cars available for tomorrow")

    car_id = available_cars[0]["id"]

    booking_data = {
        "car_id": car_id,
        "customer_name": "John Doe",
        "customer_email": "john.doe@example.com",
        "start_date": tomorrow,
        "end_date": (date.today() + timedelta(days=2)).isoformat()
    }

    response = client.post("/bookings/", json=booking_data)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["id"] is not None


def test_create_booking_invalid_dates():
    """Test creating a booking with invalid dates."""


    booking = client.get("/cars/available?target_date=" + (date.today() + timedelta(days=5)).isoformat())
    available_cars = booking.json()["data"]
    
    booking_data = {
        "car_id": available_cars[0]["id"],
        "customer_name": "Test User",
        "customer_email": "test@example.com",
        "start_date": (date.today() + timedelta(days=5)).isoformat(),
        "end_date": (date.today() + timedelta(days=2)).isoformat()
    }

    response = client.post("/bookings/", json=booking_data)
    
    assert response.status_code == 400
    data = response.json()
    
    assert data["detail"]["status"] == "failed"
    assert "cannot be after end date" in data["detail"]["message"].lower()


def test_create_booking_with_nonexist_car():
    """Test creating a booking with a non-existent car."""

    booking_data = {
        "car_id": uuid4().hex,
        "customer_name": "Test User",
        "customer_email": "test@example.com",
        "start_date": (date.today() + timedelta(days=1)).isoformat(),
        "end_date": (date.today() + timedelta(days=2)).isoformat()
    }

    response = client.post("/bookings/", json=booking_data)

    assert response.status_code == 400
    data = response.json()
    assert data["detail"]["status"] == "failed"
    assert "was not found" in data["detail"]["message"].lower()