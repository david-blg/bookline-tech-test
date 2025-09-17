from fastapi import APIRouter, Depends, HTTPException
from app.core.logger.setup_logger import logger
from app.core.dependencies import get_booking_use_cases
from app.core.models.booking_model import BookingRequest
from app.core.exceptions import CarNotAvailableError, InvalidDateRangeError
from app.core.use_cases.booking_use_cases import BookingUseCases

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.get("/")
def get_bookings(bookings_use_cases: BookingUseCases = Depends(get_booking_use_cases)):
    """Get all bookings in the system."""
    try:
        logger.info("API request: Get all bookings")
        bookings = bookings_use_cases.get_all_bookings()
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
    booking_use_cases: BookingUseCases = Depends(get_booking_use_cases)
    ):
    """Create a new booking."""
    try:
        logger.info("API request: Create booking")
        booking = booking_use_cases.create_booking(booking_req)
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