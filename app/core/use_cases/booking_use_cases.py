from app.core.interfaces.repositories import IBookingRepository, ICarRepository
from app.core.models.booking_model import BookingRequest
from app.core.exceptions import CarNotAvailableError, InvalidDateRangeError
from typing import List, Dict
from app.core.models.car_model import CarStatus


class BookingUseCases:
    def __init__(self, booking_repo: IBookingRepository, car_repo: ICarRepository):
        self.booking_repo = booking_repo
        self.car_repo = car_repo


    def get_all_bookings(self) -> List[Dict]:
        return self.booking_repo.get_all()

    def create_booking(self, booking_req: BookingRequest):
        try:
            self.booking_repo.create(booking_req)
            self.car_repo.update_status(booking_req.car_id, CarStatus.RESERVED)
        except (CarNotAvailableError, InvalidDateRangeError) as e:
            raise e
        except Exception as e:
            raise e