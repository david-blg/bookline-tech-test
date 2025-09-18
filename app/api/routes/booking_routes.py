from fastapi import APIRouter, Depends, HTTPException
from app.core.logger.setup_logger import logger
from app.core.dependencies import get_booking_use_cases
from app.core.models.booking_model import BookingRequest, ListBookingsResponse, BookingResponse
from app.core.exceptions import CarNotAvailableError, InvalidDateRangeError
from app.core.use_cases.booking_use_cases import BookingUseCases
from app.core.models.response_models import ErrorResponse

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.get("/", response_model=ListBookingsResponse)
def get_bookings(bookings_use_cases: BookingUseCases = Depends(get_booking_use_cases)):
    """Get all bookings in the system."""
    try:
        logger.info("API request: Get all bookings")
        bookings = bookings_use_cases.get_all_bookings()
        logger.info(f"API response: Retrieved {len(bookings)} bookings")
        response = ListBookingsResponse(
            status="success",
            data=bookings,
            message=f"Retrieved {len(bookings)} bookings successfully",
            total_count=len(bookings)
        )
        return response
    except Exception as e:
        err_msg = f"Unexpected error in get_bookings: {e}"
        logger.error(err_msg)
        error_response = ErrorResponse(
            error_code="INTERNAL_SERVER_ERROR",
            message=err_msg,
            status_code=500,
            status="failed"
        )
        raise HTTPException(
            status_code=error_response.status_code, 
            detail=error_response.model_dump()
        )


@router.post("/", response_model=BookingResponse)
def create_booking(
    booking_req: BookingRequest,
    booking_use_cases: BookingUseCases = Depends(get_booking_use_cases)
):
    """Create a new booking."""
    try:
        logger.info("API request: Create booking")
        booking = booking_use_cases.create_booking(booking_req)
        logger.info(f"API response: Created booking {booking['id']}")

        response = BookingResponse(
            status="success",
            data=booking,
            message="Booking created successfully"
        )
        return response
    except (CarNotAvailableError, InvalidDateRangeError) as e:
        logger.error(f"Booking creation failed: {e}")

        err_msg = f"Booking creation failed: {e}"

        error_response = ErrorResponse(
            error_code="BOOKING_CREATION_FAILED",
            message=err_msg,
            status_code=400,
            status="failed"
        )
        raise HTTPException(status_code=400, detail=error_response.model_dump())
    except Exception as e:
        logger.error(f"Unexpected error in create_booking: {e}")

        err_msg = f"Unexpected error in create_booking: {e}"

        error_response = ErrorResponse(
            error_code="INTERNAL_SERVER_ERROR",
            message=err_msg,
            status_code=500,
            status="failed"
        )
        raise HTTPException(status_code=500, detail=error_response.model_dump())