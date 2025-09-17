from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from uuid import UUID
from datetime import date

class ICarRepository(ABC):
    """Interface for car data access operations"""
    
    @abstractmethod
    def get_all(self) -> List[Dict]:
        pass
    
    @abstractmethod
    def get_by_id(self, car_id: UUID) -> Optional[Dict]:
        pass
    
    @abstractmethod
    def update_status(self, car_id: UUID, status: str) -> None:
        pass

class IBookingRepository(ABC):
    """Interface for booking data access operations"""
    
    @abstractmethod
    def get_all(self) -> List[Dict]:
        pass
    
    @abstractmethod
    def create(self, booking_data: Dict) -> Dict:
        pass
    
    @abstractmethod
    def get_by_date(self, target_date: date) -> List[Dict]:
        pass
    
    @abstractmethod
    def get_by_car_id(self, car_id: UUID) -> List[Dict]:
        pass
