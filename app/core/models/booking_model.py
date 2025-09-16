from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import date


class BaseBooking(BaseModel):
    """Shared fields for booking requests and responses."""
    car_id: UUID
    customer_name: str
    customer_email: EmailStr
    start_date: date
    end_date: date