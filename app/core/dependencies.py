from app.infra.db import JSONDatabase
from app.core.repositories.json_repositories import JSONCarRepository, JSONBookingRepository
from app.core.services.car_rental_service import CarRentalService
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

def get_car_rental_service(
    car_repo: JSONCarRepository = Depends(get_car_repository),
    booking_repo: JSONBookingRepository = Depends(get_booking_repository)
):
    """Dependency for car rental service"""
    return CarRentalService(car_repo, booking_repo)