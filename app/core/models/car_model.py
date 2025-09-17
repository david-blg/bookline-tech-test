from uuid import UUID
from pydantic import BaseModel, ConfigDict
from enum import Enum

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