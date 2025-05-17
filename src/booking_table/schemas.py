# from enum import Enum
from datetime import datetime
from pydantic import validator, BaseModel
import uuid


class CreateBookingModel(BaseModel):
    start_date: datetime
    end_date: datetime

    @validator("end_date")
    def validate_dates(cls, end_date, values):
        start_date = values.get("start_date")
        if start_date and end_date <= start_date:
            raise ValueError("End date must be after start date.")
        return end_date


# for the logic of start date and end date we can do method overloading also
# or this built-in method also can be used


class BookingResponseModel(CreateBookingModel):
    uid: uuid.UUID
    customer_id: uuid.UUID
    car_id: uuid.UUID
