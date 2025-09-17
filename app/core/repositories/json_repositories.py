from datetime import date
from typing import List, Optional
from uuid import UUID
from app.core.interfaces.repositories import ICarRepository, IBookingRepository
from app.infra.db import JSONDatabase

class JSONCarRepository(ICarRepository):
    def __init__(self, db: JSONDatabase):
        self.db = db

    def get_all(self) -> List[dict]:
        return self.db.get_all_cars()

    def get_by_id(self, car_id: UUID) -> Optional[dict]:
        return self.db.get_car_by_id(car_id)

    def update_status(self, car_id: UUID, status: str) -> None:
        self.db.set_status_car(car_id, status)

class JSONBookingRepository(IBookingRepository):
    def __init__(self, db: JSONDatabase):
        self.db = db

    def get_all(self) -> List[dict]:
        return self.db.get_all_bookings()

    def create(self, booking_data: dict) -> dict:
        self.db.add_booking(booking_data)
        return booking_data

    def get_by_date(self, target_date: date) -> List[dict]:
        all_bookings = self.get_all()
        return [
            booking for booking in all_bookings
            if booking['start_date'] <= target_date.isoformat() <= booking['end_date']
        ]