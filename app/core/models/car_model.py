from uuid import UUID
from pydantic import BaseModel, ConfigDict


class Car(BaseModel):
    id: UUID
    brand: str
    model: str
    engine: str
    version: str
    year: int
    status: str

    model_config = ConfigDict(from_attributes=True)