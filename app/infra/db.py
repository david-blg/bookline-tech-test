from pathlib import Path
from uuid import uuid4
import json

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
                        "status": "available(enum here)"
                    },
                    {
                        "id": uuid4(),
                        "brand": "Toyota",
                        "model": "Supra",
                        "engine": "2JZ-GTE",
                        "version": "MK4",
                        "year": "1996",
                        "status": "available(enum here)"
                    },
                    {
                        "id": uuid4(),
                        "brand": "BMW",
                        "model": "M3",
                        "engine": "S54B32",
                        "version": "E46",
                        "year": 2003,
                        "status": "maintenance(enum here)"
                    }
                ],
                "bookings": []
            }
            self.file_path.write_text(json.dumps(initial_data))
            print("Database file created successfully")

        def _read_data(self):
            try:
                if not self.file_path.exists():
                    return None
                with open(self.file_path, "r") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error reading data from file: {e}")
                return None

        def _write_data(self, data):
            try:
                with open(self.file_path, "w") as f:
                    json.dump(data, f, indent=4)
            except Exception as e:
                print(f"Error writing data to file: {e}")


        def get_all_cars(self):
            data = self._read_data()
            return data.get("cars", [])


        def get_all_bookings(self):
            data = self._read_data()
            return data.get("bookings", [])