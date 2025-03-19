from pydantic import BaseModel


class CarCreateModel(BaseModel):
    name: str
    model: str
    brand: str
    category: str
    price_per_day: float
    engine: str
    fuelType: str
    siting_capacity: int


class CarGetModel(CarCreateModel):
    id: int
