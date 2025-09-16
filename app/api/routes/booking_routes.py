from fastapi import APIRouter, Depends, HTTPException
from app.core.logger.setup_logger import logger
from app.core.services.car_rental_service import CarRentalService
from app.infra.db import JSONDatabase
from app.core.models.booking_model import BookingRequest
from app.core.exceptions import CarNotAvailableError, InvalidDateRangeError

router = APIRouter(prefix="/bookings", tags=["bookings"])

def get_database():
    return JSONDatabase()

def get_car_service(db: JSONDatabase = Depends(get_database)):
    return CarRentalService(db)

@router.get("/")
def get_bookings(service: CarRentalService = Depends(get_car_service)):
    """Get all bookings in the system."""
    try:
        logger.info("API request: Get all bookings")
        bookings = service.get_all_bookings()
        logger.info(f"API response: Retrieved {len(bookings)} bookings")
        response = {
            "bookings": bookings,
            "total_count": len(bookings)
        }
        return response
    except Exception as e:
        logger.error(f"Unexpected error in get_bookings: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/")
def create_booking(
    booking_req: BookingRequest,
    service: CarRentalService = Depends(get_car_service)
    ):
    """Create a new booking."""
    try:
        logger.info("API request: Create booking")
        booking = service.create_booking(booking_req)
        logger.info(f"API response: Created booking {booking['id']}")
        return {
            "status": "success",
            "data": booking,
            "message": "Booking created successfully"
        }
    except (CarNotAvailableError, InvalidDateRangeError) as e:
        logger.error(f"Booking creation failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in create_booking: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")