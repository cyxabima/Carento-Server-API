# from enum import Enum
from datetime import datetime
from pydantic import validator, BaseModel
import uuid

from src.db.models import Cars


class CreateBookingModel(BaseModel):
    start_date: datetime
    end_date: datetime
    no_of_days: int

    @validator("end_date")
    def validate_dates(cls, end_date, values):
        start_date = values.get("start_date")
        if start_date and end_date <= start_date:
            raise ValueError("End date must be after start date.")
        return end_date


# for the logic of start date and end date we can do method overloading also
# or this built-in method also can be used


class BookingResponseModel(BaseModel):
    uid: uuid.UUID
    start_date: datetime
    end_date: datetime
    customer_id: uuid.UUID
    car_id: uuid.UUID
    is_active: bool
    total_price: float
    car: Cars
