from fastapi import APIRouter, Depends, Query, HTTPException
from app.core.dependencies import get_car_use_cases
from app.core.logger.setup_logger import logger
from datetime import date
from app.core.exceptions import InvalidDateRangeError
from app.core.models.response_models import CarsListResponse, AvailableCarsResponse, ErrorResponse
from app.core.use_cases.car_use_cases import CarUseCases

router = APIRouter(prefix="/cars", tags=["cars"])

@router.get("/", response_model=CarsListResponse)
def get_all_cars(car_use_case: CarUseCases = Depends(get_car_use_cases)):
    """
    Get all cars
    """
    logger.info("API request: Get all cars")

    try:
        cars = car_use_case.get_all_cars()
        logger.info(f"API response: Retrieved {len(cars)} cars")        
        response = CarsListResponse(
            status="success",
            data=cars,
            message=f"Retrieved {len(cars)} cars successfully",
            total_count=len(cars)
        )
        return response
    except Exception as e:
        logger.error(f"Unexpected error in get_all_cars: {e}")
        raise HTTPException(
            status_code=500, 
            detail=ErrorResponse(
                error_code="CARS_RETRIEVAL_ERROR",
                message="Error retrieving cars"
            )
        )


@router.get("/available", response_model=AvailableCarsResponse)
def list_available_cars(
    car_use_case: CarUseCases = Depends(get_car_use_cases), 
    target_date: date = Query(...)
):
    """
    List available cars for a specific date
    """

    try:
        logger.info(f"API request: List available cars for date: {target_date}")
        available_cars = car_use_case.get_available_cars(target_date)
        response = AvailableCarsResponse(
            status="success",
            data=available_cars,
            message=f"Retrieved {len(available_cars)} available cars for {target_date}",
            total_count=len(available_cars)
        )

        logger.info(f"API response: Retrieved {len(available_cars)} available cars for {target_date}")
        return response
    except InvalidDateRangeError as e:
        logger.error(f"Invalid date range error: {e}")
        error_response = ErrorResponse(
            error_code="INVALID_DATE_RANGE",
            message=str(e),
            status_code=400,
            status="failed"
        )
        raise HTTPException(
            status_code=error_response.status_code, 
            detail=error_response.model_dump()
        )
    except Exception as e:
        logger.error(f"Unexpected error in list_available_cars: {e}")
        error_response = ErrorResponse(
            error_code="INTERNAL_SERVER_ERROR",
            message="Internal server error",
            status_code=500,
            status="failed"
        )
        raise HTTPException(
            status_code=error_response.status_code, 
            detail=error_response.model_dump()
        )