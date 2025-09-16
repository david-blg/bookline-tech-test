from fastapi import APIRouter
from app.core.logger.setup_logger import logger

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.get("/")
def get_bookings():
    logger.info("Getting all bookings")
    return {"message": "get bookings"}