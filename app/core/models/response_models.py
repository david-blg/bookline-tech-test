from pydantic import BaseModel
from typing import List, Dict

class CarsListResponse(BaseModel):
    """Response for list of cars"""
    status: str = "success"
    message: str = "Cars retrieved successfully"
    data: List[Dict]
    total_count: int

class AvailableCarsResponse(BaseModel):
    """Response for available cars"""
    status: str = "success"
    message: str = "Available cars retrieved successfully"
    data: List[Dict]
    total_count: int