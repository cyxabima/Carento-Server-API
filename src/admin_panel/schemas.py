from pydantic import BaseModel, EmailStr
import uuid
from datetime import datetime
from typing import Optional
from src.vehicles.schemas import CarGetModel


class ContactGetModel(BaseModel):
    name: str
    email: EmailStr
    message: str


class AdminGetModel(BaseModel):
    name: str
    password: str


class ReviewGetModel(BaseModel):
    uid: uuid.UUID
    customer_id: uuid.UUID
    car_id: uuid.UUID
    rating: int
    review_text: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class BookingGetModel(BaseModel):
    uid: uuid.UUID
    customer_id: uuid.UUID
    car_id: uuid.UUID
    start_date: datetime
    end_date: datetime
    total_price: float
    is_payment_confirmed: bool


class AdminCarGetModel(CarGetModel):
    pass


class VendorGetModel(BaseModel):
    uid: uuid.UUID
    email: EmailStr
    phone_no: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    business_name: Optional[str] = None
    is_business: bool
    created_at: datetime
    updated_at: datetime


class CustomerGetModel(BaseModel):
    uid: uuid.UUID
    email: EmailStr
    phone_no: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class UserDeleteModel(BaseModel):
    email: EmailStr
