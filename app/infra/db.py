import json
from app.core.logger.setup_logger import logger
from pathlib import Path
from typing import Dict, List, Any
from uuid import uuid4, UUID
from app.core.models.car_model import CarStatus

class JSONDatabase:
    def __init__(self, file_path: str = "app/data/db.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Create a new file if it doesn't exist"""
        if not self.file_path.exists():
            initial_data = {
                "cars": [
                    {
                        "id": uuid4(),
                        "brand": "Toyota",
                        "model": "Chaser",
                        "engine": "JZX100 1JZ-GTE",
                        "version": "Tourer V",
                        "year": "1998",
                        "status": CarStatus.AVAILABLE
                    },
                    {
                        "id": uuid4(),
                        "brand": "Toyota",
                        "model": "Supra",
                        "engine": "2JZ-GTE",
                        "version": "MK4",
                        "year": "1996",
                        "status": CarStatus.AVAILABLE
                    },
                    {
                        "id": uuid4(),
                        "brand": "BMW",
                        "model": "M3",
                        "engine": "S54B32",
                        "version": "E46",
                        "year": 2003,
                        "status": CarStatus.MAINTENANCE
                    }
                ],
                "bookings": []
            }
            self._write_data(initial_data)
            logger.info(f"Created new database file at {self.file_path}")

    def _read_data(self) -> Dict[str, List[Any]]:
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Error reading database file: {e}. Returning empty data.")
            return {"cars": [], "bookings": []}

    def _write_data(self, data: Dict[str, List[Any]]):
        try:
            with open(self.file_path, 'w') as file:
                json.dump(data, file, indent=4, default=str)
        except Exception as e:
            logger.error(f"Error writing to database file: {e}")
            raise

    def get_all_cars(self) -> List[Dict]:
        data = self._read_data()
        return data.get("cars", [])
    
    def get_car_by_id(self, car_id: UUID) -> Dict:
        data = self._read_data()
        for car in data.get("cars", []):
            if car['id'] == str(car_id):
                return car
        return None
    
    def get_all_bookings(self) -> List[Dict]:
        data = self._read_data()
        return data.get("bookings", [])

    def add_booking(self, booking: Dict) -> None:
        data = self._read_data()
        data["bookings"].append(booking)
        self._write_data(data)
        logger.info(f"New booking added: {booking['id']}")


    def set_status_car(self, car_id: UUID, status: CarStatus) -> None:
        data = self._read_data()
        for car in data.get("cars", []):
            if car['id'] == str(car_id):
                car['status'] = status.value
                self._write_data(data)
                logger.info(f"Car {car_id} status updated to {status.value}")
                return