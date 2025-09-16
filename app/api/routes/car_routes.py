from fastapi import APIRouter, Depends, Query, HTTPException
from app.core.services.car_rental_service import CarRentalService
from app.infra.db import JSONDatabase
from app.core.logger.setup_logger import logger
from datetime import date

router = APIRouter(prefix="/cars", tags=["cars"])

def get_database():
    return JSONDatabase()

def get_car_service(db: JSONDatabase = Depends(get_database)):
    return CarRentalService(db)

@router.get("/")
def get_all_cars(car_service: CarRentalService = Depends(get_car_service)):
    """
    Get all cars
    """
    try:
        logger.info("API request: Get all cars")
        cars = car_service.get_all_cars()
        logger.info(f"API response: Retrieved {len(cars)} cars")
        return {
            "status": "success",
            "data": cars,
            "total_count": len(cars)
        }
    except Exception as e:
        logger.error(f"Error getting all cars: {e}")
        raise HTTPException(status_code=500, detail="Error getting all cars")


@router.get("/available")
def list_available_cars(
    car_service: CarRentalService = Depends(get_car_service), 
    target_date: date = Query(...)
):
    """
    List available cars for a specific date
    """

    try:
        logger.info(f"API request: List available cars for date: {target_date}")
        available_cars = car_service.get_available_cars_for_date(target_date)
        logger.info(f"API response: Retrieved {len(available_cars)} available cars for {target_date}")
        return {
            "status": "success",
            "data": available_cars,
            "total_count": len(available_cars)
        }
    except Exception as e:
        logger.error(f"Error listing available cars: {e}")
        raise HTTPException(status_code=500, detail="Error listing available cars")