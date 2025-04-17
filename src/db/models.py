from datetime import datetime
from typing import Optional, List
import uuid
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr
from src.booking_table.schemas import BookingStatus


# ---------------------- CARS MODEL ----------------------
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
    is_booked: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationship with Reviews
    reviews: List["Reviews"] = Relationship(
        back_populates="car", sa_relationship_kwargs={"lazy": "selectin"}
    )


# ---------------------- BASE USER MODEL ----------------------
class BaseUser(SQLModel):
    uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: EmailStr
    password: str
    phone_no: str


# ---------------------- CUSTOMERS MODEL ----------------------
class Customers(BaseUser, table=True):
    first_name: str
    last_name: str
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationship with Reviews
    reviews: List["Reviews"] = Relationship(
        back_populates="customer", sa_relationship_kwargs={"lazy": "selectin"}
    )


# ---------------------- VENDORS MODEL ----------------------
class Vendors(BaseUser, table=True):
    first_name: Optional[str] = None  # For individuals
    last_name: Optional[str] = None  # For individuals
    business_name: Optional[str] = None  # For businesses
    is_business: bool
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


# ---------------------- REVIEWS MODEL ----------------------
class Reviews(SQLModel, table=True):
    uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    customer_id: uuid.UUID = Field(foreign_key="customers.uid")
    car_id: uuid.UUID = Field(foreign_key="cars.uid")

    rating: int = Field(..., ge=1, le=5)  # Rating between 1 and 5
    review_text: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    customer: "Customers" = Relationship(
        back_populates="reviews", sa_relationship_kwargs={"lazy": "selectin"}
    )
    car: "Cars" = Relationship(
        back_populates="reviews", sa_relationship_kwargs={"lazy": "selectin"}
    )


# ---------------------- BOOKING TABLE ----------------------
class Booking(SQLModel, table=True):
    uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    customer_id: uuid.UUID = Field(foreign_key="customers.uid")
    car_id: uuid.UUID = Field(foreign_key="cars.uid")
    start_date: datetime
    end_date: datetime
    total_price: float
    is_payment_confirmed: bool = Field(default=False)


# ---------------------- ADMIN TABLE ----------------------

class Admin(SQLModel, table=True):
    pass