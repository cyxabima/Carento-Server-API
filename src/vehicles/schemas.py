from datetime import datetime
from typing import Optional
import uuid
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
    uid: uuid.UUID
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
