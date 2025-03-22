from pydantic import BaseModel, EmailStr
from datetime import datetime
import uuid
from typing import Optional


class UserCreateModel(BaseModel):
    email: EmailStr
    password: str
    phone_no: str


class UserLoginModel(BaseModel):
    email: EmailStr
    password: str
    phone_no: Optional[str] = None


class CustomerCreateModel(UserCreateModel):
    first_name: str
    last_name: str


class CustomerGetModel(CustomerCreateModel):
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime


class VendorCreateModel(UserCreateModel):
    first_name: Optional[str] = None  # For individuals
    last_name: Optional[str] = None  # For individuals
    business_name: Optional[str] = None  # For businesses
    is_business: bool


class VendorGetModel(VendorCreateModel):
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime


class token(BaseModel):
    access_token: str
    token_type: str


class token_data(BaseModel):
    id: Optional[str] = None
