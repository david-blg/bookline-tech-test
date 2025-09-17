from pydantic import BaseModel
from typing import Dict, Generic, Optional, TypeVar

T = TypeVar('T')

class BaseResponse(BaseModel):
    """Base response model"""
    status: str
    message: str

class SuccessResponse(BaseResponse, Generic[T]):
    """Success response model"""
    data: T
    total_count: Optional[int] = None

class ErrorResponse(BaseResponse):
    """Error response model"""
    error_code: str
    details: Optional[Dict[str, str]] = None
