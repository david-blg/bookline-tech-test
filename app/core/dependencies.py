from app.infra.db import JSONDatabase
from app.core.repositories.json_repositories import JSONCarRepository, JSONBookingRepository
from app.core.use_cases.car_use_cases import CarUseCases
from app.core.use_cases.booking_use_cases import BookingUseCases
from fastapi import Depends

def get_json_database():
    """Dependency for JSON database"""
    return JSONDatabase()

def get_car_repository(db: JSONDatabase = Depends(get_json_database)):
    """Dependency for car repository"""
    return JSONCarRepository(db)

def get_booking_repository(db: JSONDatabase = Depends(get_json_database)):
    """Dependency for booking repository"""
    return JSONBookingRepository(db)

def get_car_use_cases(
    car_repo: JSONCarRepository = Depends(get_car_repository),
    booking_repo: JSONBookingRepository = Depends(get_booking_repository)
):
    """Dependency for car use cases"""
    return CarUseCases(car_repo, booking_repo)


def get_booking_use_cases(
    booking_repo: JSONBookingRepository = Depends(get_booking_repository),
    car_repo: JSONCarRepository = Depends(get_car_repository)
):
    """Dependency for booking use cases"""
    return BookingUseCases(booking_repo, car_repo)
