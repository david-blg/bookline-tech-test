from pydantic import BaseModel, EmailStr, ConfigDict, field_validator
from uuid import UUID
from datetime import date, datetime


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