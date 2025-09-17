from uuid import UUID
from pydantic import BaseModel, ConfigDict
from enum import Enum
from app.core.models.response_models import BaseResponse
from typing import List

class CarStatus(str, Enum):
    """Car status enum"""
    AVAILABLE = "available"
    RESERVED = "reserved"
    MAINTENANCE = "maintenance"


class Car(BaseModel):
    """Car model"""
    id: UUID
    brand: str
    model: str
    engine: str
    version: str
    year: int
    status: CarStatus = CarStatus.AVAILABLE

    model_config = ConfigDict(from_attributes=True)


class CarsListResponse(BaseResponse):
    """Response for list of cars"""
    data: List[Car]
    total_count: int

class AvailableCarsResponse(BaseResponse):
    """Response for available cars"""
    data: List[Car]
    total_count: int