from datetime import datetime
from typing import Optional
import uuid
from sqlmodel import SQLModel, Field
from pydantic import EmailStr


class Cars(SQLModel, table=True):
    uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    model: str
    brand: str
    category: str
    engine: str
    fuelType: str
    siting_capacity: int
    price_per_day: float
    created_at: datetime = Field(nullable=False, default=datetime.now())
    updated_at: datetime = Field(nullable=False, default=datetime.now())


class BaseUser(SQLModel):
    uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: EmailStr = Field(unique=True)
    password: str
    phone_no: str


class Customers(BaseUser, table=True):
    first_name: str
    last_name: str
    created_at: datetime = Field(nullable=False, default=datetime.now())
    updated_at: datetime = Field(nullable=False, default=datetime.now())


class Vendors(BaseUser, table=True):
    first_name: Optional[str] = None  # For individuals
    last_name: Optional[str] = None  # For individuals
    business_name: Optional[str] = None  # For businesses
    is_business: bool
    created_at: datetime = Field(nullable=False, default=datetime.now())
    updated_at: datetime = Field(nullable=False, default=datetime.now())
