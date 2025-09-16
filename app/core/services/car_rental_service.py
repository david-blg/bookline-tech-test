from datetime import date
from typing import List, Dict
from uuid import UUID
from app.core.logger.setup_logger import setup_logger
from app.infra.db import JSONDatabase
from app.core.models.car_model import CarStatus
from app.core.exceptions import InvalidDateRangeError


class CarRentalService:
    """Service for car rental"""

    def __init__(self, db: JSONDatabase):
        self.logger = setup_logger("car_rental_service")
        self.db = db

    def get_all_cars(self) -> List[Dict]:
        self.logger.info("Getting all cars")
        cars = self.db.get_all_cars()
        self.logger.info(f"Found {len(cars)} cars")
        return cars

    def get_all_bookings(self) -> List[Dict]:
        self.logger.info("Getting all bookings")
        bookings = self.db.get_all_bookings()
        self.logger.info(f"Found {len(bookings)} bookings")
        return bookings


    def is_car_available(self, car_id: UUID) -> bool:
        self.logger.info(f"Checking availability for car {car_id}")
        car = self.db.get_car_by_id(car_id)
        if not car:
            self.logger.info(f"Car {car_id} not found")
            return False
        if car["status"] == CarStatus.MAINTENANCE:
            self.logger.info(f"Car {car_id} is in maintenance")
            return False
        return True


    def get_available_cars_for_date(self, target_date: date) -> List[Dict]:
        """
        Get available cars for a specific date
        """
        self.logger.info(f"Getting available cars for date {target_date}")

        if target_date < date.today():
            self.logger.error(f"Attempted to query availability for past date: {target_date}")
            raise InvalidDateRangeError("Cannot check availability for past dates")

        all_cars = self.get_all_cars()
        all_bookings = self.get_all_bookings()

        available_cars = []
        for car in all_cars:
            car_id = car["id"]
            if car["status"] != CarStatus.AVAILABLE:
                continue

            is_available = True

            for booking in all_bookings:
                if booking["car_id"] == car_id:
                    start_date = date.fromisoformat(booking['start_date']) if isinstance(booking['start_date'], str) else booking['start_date']
                    end_date = date.fromisoformat(booking['end_date']) if isinstance(booking['end_date'], str) else booking['end_date']
                    
                    if start_date <= target_date <= end_date:
                        self.logger.debug(f"Car {car_id} is booked on {target_date}")
                        is_available = False
                        break

            if is_available:
                available_cars.append(car)
        
        self.logger.info(f"Found {len(available_cars)} cars available for {target_date}")
        return available_cars