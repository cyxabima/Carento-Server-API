from datetime import datetime
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

class Users(SQLModel, table=True):
    uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    phone_no: str
    created_at: datetime = Field(nullable=False, default=datetime.now())
    updated_at: datetime = Field(nullable=False, default=datetime.now())