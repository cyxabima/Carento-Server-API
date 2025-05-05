from datetime import datetime
from typing import List, Literal, Optional
import uuid
from pydantic import BaseModel

from src.db.models import Reviews


class CarCreateModel(BaseModel):
    car_name: str
    model_year: str
    image_url: str
    brand: str
    car_category: str
    engine_size: str
    fuel_type: str
    siting_capacity: int
    price_per_day: float
    registration_no: str
    transmission: Literal["Manual", "Automatic"]


class CarGetModel(CarCreateModel):
    uid: uuid.UUID
    reviews: List[Reviews]
    created_at: datetime
    updated_at: datetime


class CarUpdateModel(BaseModel):
    # why default value as we are using this in patch operation where client may not provide all values
    # he can only provide the value which he want to upgrade
    name: Optional[str] = None
    model: Optional[str] = None
    brand: Optional[str] = None
    category: Optional[str] = None
    price_per_day: Optional[float] = None
    engine: Optional[str] = None
    fuelType: Optional[str] = None
    siting_capacity: Optional[int] = None
