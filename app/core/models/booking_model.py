from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import date
from typing import List
from app.core.models.response_models import BaseResponse


class BaseBooking(BaseModel):
    """Shared fields for booking requests and responses."""
    car_id: UUID
    customer_name: str
    customer_email: EmailStr
    start_date: date
    end_date: date

class BookingRequest(BaseBooking):
    """Booking request model."""
    pass

class Booking(BaseBooking):
    """Booking model."""
    id: UUID

class ListBookingsResponse(BaseResponse):
    """List bookings response model."""
    data: List[Booking]
    total_count: int


class BookingResponse(BaseResponse):
    """Booking response model."""
    data: Booking
