from fastapi import APIRouter, Depends, Query, HTTPException
from app.core.dependencies import get_car_rental_service
from app.core.services.car_rental_service import CarRentalService
from app.core.logger.setup_logger import logger
from datetime import date
from app.core.exceptions import InvalidDateRangeError
from app.core.models.response_models import CarsListResponse, AvailableCarsResponse


router = APIRouter(prefix="/cars", tags=["cars"])

@router.get("/", response_model=CarsListResponse)
def get_all_cars(car_service: CarRentalService = Depends(get_car_rental_service)):
    """
    Get all cars
    """
    try:
        logger.info("API request: Get all cars")
        cars = car_service.get_all_cars()
        logger.info(f"API response: Retrieved {len(cars)} cars")
        response = CarsListResponse(
            status="success",
            data=cars,
            total_count=len(cars)
        )
        return response
    except Exception as e:
        logger.error(f"Error getting all cars: {e}")
        raise HTTPException(status_code=500, detail="Error getting all cars")


@router.get("/available", response_model=AvailableCarsResponse)
def list_available_cars(
    car_service: CarRentalService = Depends(get_car_rental_service), 
    target_date: date = Query(...)
):
    """
    List available cars for a specific date
    """

    try:
        logger.info(f"API request: List available cars for date: {target_date}")
        available_cars = car_service.get_available_cars_for_date(target_date)
        response = CarsListResponse(
            status="success",
            data=available_cars,
            total_count=len(available_cars)
        )

        logger.info(f"API response: Retrieved {len(available_cars)} available cars for {target_date}")
        return response
    except InvalidDateRangeError as e:
        logger.error(f"Invalid date range error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in list_available_cars: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")