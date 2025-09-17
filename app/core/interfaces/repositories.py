from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from datetime import date

class ICarRepository(ABC):
    """Interface for car data access operations"""
    
    @abstractmethod
    def get_all(self) -> List[dict]:
        pass
    
    @abstractmethod
    def get_by_id(self, car_id: UUID) -> Optional[dict]:
        pass
    
    @abstractmethod
    def update_status(self, car_id: UUID, status: str) -> None:
        pass

class IBookingRepository(ABC):
    """Interface for booking data access operations"""
    
    @abstractmethod
    def get_all(self) -> List[dict]:
        pass
    
    @abstractmethod
    def create(self, booking_data: dict) -> dict:
        pass
    
    @abstractmethod
    def get_by_date(self, target_date: date) -> List[dict]:
        pass