from pydantic import BaseModel

class BaseResponse(BaseModel):
    """Base response model"""
    status: str = "success"
    message: str = "Operation successful"

class ErrorResponse(BaseResponse):
    """Error response model"""
    error_code: str
    message: str = "Operation failed"
    status_code: int = 500