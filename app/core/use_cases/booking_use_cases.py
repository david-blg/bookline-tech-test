from app.core.interfaces.repositories import IBookingRepository, ICarRepository
from app.core.models.booking_model import BookingRequest
from app.core.exceptions import CarNotAvailableError, InvalidDateRangeError
from typing import List, Dict
from app.core.models.car_model import CarStatus
from app.core.logger.setup_logger import logger
from uuid import uuid4, UUID
from datetime import datetime, date

class BookingUseCases:
    def __init__(self, booking_repo: IBookingRepository, car_repo: ICarRepository):
        self.booking_repo = booking_repo
        self.car_repo = car_repo

    def get_all_bookings(self) -> List[Dict]:
        """Get all bookings"""
        return self.booking_repo.get_all()

    def validate_booking_dates(self, start_date: date, end_date: date) -> None:
        """Validate booking dates with descriptive error messages"""
        today = date.today()
        
        if start_date < today:
            raise InvalidDateRangeError(
                f"Cannot book for past dates. Selected date: {start_date}, Today: {today}"
            )
        
        if start_date > end_date:
            raise InvalidDateRangeError(
                f"Start date ({start_date}) cannot be after end date ({end_date})"
            )

    def is_car_booked(self, car_id: UUID, start_date: date, end_date: date) -> bool:
        """Check if a car is already booked for the given date range"""
        bookings = self.booking_repo.get_by_car_id(car_id)
        
        for booking in bookings:
            try:
                existing_start = date.fromisoformat(booking['start_date'])
                existing_end = date.fromisoformat(booking['end_date'])
                
                if not (end_date < existing_start or start_date > existing_end):
                    logger.info(
                        f"Car {car_id} has overlapping booking: "
                        f"{existing_start} to {existing_end} conflicts with "
                        f"{start_date} to {end_date}"
                    )
                    return True
                    
            except (ValueError, KeyError) as e:
                logger.warning(f"Invalid booking data format: {e}")
                continue
        
        return False

    def _check_car_availability(self, car_id: UUID) -> None:
        """Check if car exists and is available with descriptive errors"""
        car = self.car_repo.get_by_id(car_id)
        
        if not car:
            logger.warning(f"Car {car_id} not found in database")
            raise CarNotAvailableError(f"Car with ID {car_id} was not found")
        
        if car['status'] != CarStatus.AVAILABLE:
            current_status = car['status']
            logger.info(f"Car {car_id} is not available. Current status: {current_status}")
            raise CarNotAvailableError(
                f"Car with ID {car_id} is not available. Current status: {current_status}"
            )

    def is_car_available_for_dates(self, car_id: UUID, start_date: date, end_date: date) -> bool:
        """Check if car is available for the specific date range"""

        if self.is_car_booked(car_id, start_date, end_date):
            logger.info(
                f"Car {car_id} is already booked for the selected dates: "
                f"{start_date} to {end_date}"
            )
            return False
        
        return True

    def create_booking(self, booking_req: BookingRequest) -> Dict:
        """Create a new booking with comprehensive validation"""
        try:
            logger.info(
                f"Starting booking creation for car {booking_req.car_id} "
                f"from {booking_req.start_date} to {booking_req.end_date}"
            )
            
            self._check_car_availability(booking_req.car_id)
            logger.info(f"Car {booking_req.car_id} status validation passed")
            
            self.validate_booking_dates(booking_req.start_date, booking_req.end_date)
            logger.info("Booking date validation passed")
            
            if not self.is_car_available_for_dates(booking_req.car_id, booking_req.start_date, booking_req.end_date):
                raise CarNotAvailableError(
                    f"Car {booking_req.car_id} is already booked for the selected dates: "
                    f"{booking_req.start_date} to {booking_req.end_date}"
                )
            logger.info("Car availability for dates validation passed")
            
            booking_data = booking_req.model_dump()
            booking_data['id'] = uuid4()
            booking_data['created_at'] = datetime.now().isoformat()
            
            logger.info(f"Creating booking with ID: {booking_data['id']}")
            
            created_booking = self.booking_repo.create(booking_data)
            
            self.car_repo.update_status(booking_req.car_id, CarStatus.RESERVED)
            logger.info(f"Car {booking_req.car_id} status updated to {CarStatus.RESERVED}")
            
            logger.info(
                f"Booking {created_booking['id']} created successfully for "
                f"car {booking_req.car_id} from {booking_req.start_date} to {booking_req.end_date}"
            )
            
            return created_booking
            
        except (CarNotAvailableError, InvalidDateRangeError) as e:
            logger.error(f"Booking creation failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error in create_booking: {str(e)}", 
                exc_info=True,
                extra={'car_id': booking_req.car_id if 'booking_req' in locals() else 'unknown'}
            )
            raise