from app.core.interfaces.repositories import ICarRepository
from app.core.exceptions import InvalidDateRangeError
from app.core.logger.setup_logger import logger
from datetime import date
from typing import List, Dict
from app.core.interfaces.repositories import IBookingRepository
from app.core.models.car_model import CarStatus

class CarUseCases:
    def __init__(self, car_repo: ICarRepository, booking_repo: IBookingRepository):
        self.car_repo = car_repo
        self.booking_repo = booking_repo

    def get_all_cars(self) -> List[Dict]:
        return[car for car in self.car_repo.get_all() if car['status'] == CarStatus.AVAILABLE] 

    def get_available_cars(self, target_date: date):
        logger.info(f"Getting available cars for {target_date}")
        
        if target_date < date.today():
            raise InvalidDateRangeError("Cannot check availability for past dates")
        
        all_cars = self.car_repo.get_all()
        bookings = self.booking_repo.get_all()
         
        booked_car_ids = {booking['car_id'] for booking in bookings}
        
        available_cars = [
            car for car in all_cars 
            if car['id'] not in booked_car_ids and car['status'] == CarStatus.AVAILABLE
        ]
        
        return available_cars