from fastapi import APIRouter, Depends
from app.core.logger.setup_logger import logger
from app.core.services.car_rental_service import CarRentalService
from app.infra.db import JSONDatabase

router = APIRouter(prefix="/bookings", tags=["bookings"])

def get_database():
    return JSONDatabase()

def get_car_service(db: JSONDatabase = Depends(get_database)):
    return CarRentalService(db)

@router.get("/")
def get_bookings(car_service: CarRentalService = Depends(get_car_service)):
    logger.info("Getting all bookings")
    return car_service.get_all_bookings()