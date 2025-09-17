from datetime import date, datetime
from typing import List, Dict
from uuid import UUID, uuid4
from app.core.logger.setup_logger import logger
from app.core.models.car_model import CarStatus
from app.core.exceptions import InvalidDateRangeError, CarNotAvailableError
from app.core.models.booking_model import BookingRequest
from app.core.interfaces.repositories import ICarRepository, IBookingRepository


class CarRentalService:
    """Service for car rental"""

    def __init__(self, car_repo: ICarRepository, booking_repo: IBookingRepository):
        # self.db = db
        self.car_repo = car_repo
        self.booking_repo = booking_repo

    def get_all_cars(self) -> List[Dict]:
        logger.info("Getting all cars")
        cars = self.car_repo.get_all()
        logger.info(f"Found {len(cars)} cars")
        return cars

    def get_all_bookings(self) -> List[Dict]:
        logger.info("Getting all bookings")
        bookings = self.booking_repo.get_all()
        logger.info(f"Found {len(bookings)} bookings")
        return bookings


    def is_car_available(self, car_id: UUID) -> bool:
        logger.info(f"Checking availability for car {car_id}")
        car = self.car_repo.get_by_id(car_id)
        if not car:
            logger.info(f"Car {car_id} not found")
            return False
        if car["status"] == CarStatus.MAINTENANCE:
            logger.info(f"Car {car_id} is in maintenance")
            return False
        return True


    def get_available_cars_for_date(self, target_date: date) -> List[Dict]:
        """
        Get available cars for a specific date
        """
        logger.info(f"Getting available cars for date {target_date}")

        if target_date < date.today():
            logger.error(f"Attempted to query availability for past date: {target_date}")
            raise InvalidDateRangeError("Cannot check availability for past dates")

        all_cars = self.car_repo.get_all()
        all_bookings = self.booking_repo.get_all()

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
                        logger.debug(f"Car {car_id} is booked on {target_date}")
                        is_available = False
                        break

            if is_available:
                available_cars.append(car)
        
        logger.info(f"Found {len(available_cars)} cars available for {target_date}")
        return available_cars


    def validate_range_date(self, start_date: date, end_date: date):
        """
        Validate the date range for a booking
        """
        logger.info(f"Validating date range from {start_date} to {end_date}")
        if start_date < date.today():
            raise InvalidDateRangeError("Cannot check availability for past dates")
        if start_date > end_date:
            raise InvalidDateRangeError("Start date cannot be after end date")


    def is_car_available_for_dates(self, car_id: UUID, start_date: date, end_date: date) -> bool:
        """
        Checks if a car is available for a specific date range.
        """
        logger.info(f"Checking availability for car {car_id} from {start_date} to {end_date}")
        
        if not self.is_car_available(car_id):
            logger.info(f"Car {car_id} is not in available status")
            return False
        
        bookings = self.get_all_bookings()
        
        for booking in bookings:
            if not isinstance(booking, dict):
                logger.error(f"Invalid booking data: {booking}, type: {type(booking)}")
                continue
            
            if booking['car_id'] == str(car_id):
                existing_start = date.fromisoformat(booking['start_date']) if isinstance(booking['start_date'], str) else booking['start_date']
                existing_end = date.fromisoformat(booking['end_date']) if isinstance(booking['end_date'], str) else booking['end_date']
                
                if not (end_date < existing_start or start_date > existing_end):
                    logger.info(f"Car {car_id} is already booked from {existing_start} to {existing_end}")
                    return False
        
        logger.info(f"Car {car_id} is available for the requested dates")
        return True

    def create_booking(self, booking_request: BookingRequest) -> Dict:
        """
        Create a new booking with car availability check
        """
        logger.info(f"Creating booking for car {booking_request.car_id} from {booking_request.start_date} to {booking_request.end_date}")
        
        try:
            self.validate_range_date(booking_request.start_date, booking_request.end_date)
            
            if not self.is_car_available_for_dates(
                booking_request.car_id, 
                booking_request.start_date, 
                booking_request.end_date
            ):
                error_msg = f"Car with id {booking_request.car_id} is not available from {booking_request.start_date} to {booking_request.end_date}"
                logger.error(f"Booking creation failed: {error_msg}")
                raise CarNotAvailableError(error_msg)
            
            booking_id = uuid4()
            created_at = datetime.now()
            
            booking_data = {
                'id': str(booking_id),
                'car_id': str(booking_request.car_id),
                'customer_name': booking_request.customer_name,
                'customer_email': booking_request.customer_email,
                'start_date': booking_request.start_date.isoformat(),
                'end_date': booking_request.end_date.isoformat(),
                'created_at': created_at.isoformat()  
            }
            
            self.booking_repo.create(booking_data)
            
            logger.info(f"Booking created successfully with ID: {booking_data['id']}")

            self.car_repo.update_status(booking_request.car_id, CarStatus.RESERVED)
            return booking_data
            
        except (CarNotAvailableError, InvalidDateRangeError) as e:
            logger.error(f"Failed to create booking: {e}")
            raise