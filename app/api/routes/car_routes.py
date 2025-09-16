from fastapi import APIRouter, Depends
from app.core.services.car_rental_service import CarRentalService
from app.infra.db import JSONDatabase
from app.core.logger.setup_logger import logger

router = APIRouter(prefix="/cars", tags=["cars"])

def get_database():
    return JSONDatabase()

def get_car_service(db: JSONDatabase = Depends(get_database)):
    return CarRentalService(db)

@router.get("/")
def get_all_cars(car_service: CarRentalService = Depends(get_car_service)):
    logger.info("Getting first data cars")
    return car_service.get_all_cars()