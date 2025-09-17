from pydantic import BaseModel
from typing import List
from app.core.models.car_model import Car

class BaseResponse(BaseModel):
    """Base response model"""
    status: str = "success"
    message: str = "Operation successful"

class ErrorResponse(BaseResponse):
    """Error response model"""
    error_code: str
    message: str = "Operation failed"
    status_code: int = 500
    
class CarsListResponse(BaseResponse):
    """Response for list of cars"""
    data: List[Car]
    total_count: int

class AvailableCarsResponse(BaseResponse):
    """Response for available cars"""
    data: List[Car]
    total_count: int