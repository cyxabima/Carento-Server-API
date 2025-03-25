from datetime import datetime
from typing import Optional, List
import uuid
from sqlmodel import SQLModel, Field, Relationship
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
    reviews: List["Reviews"] = Relationship(back_populates="Cars")


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
    reviews: List["Reviews"] = Relationship(back_populates="Customers")


class Vendors(BaseUser, table=True):
    first_name: Optional[str] = None  # For individuals
    last_name: Optional[str] = None  # For individuals
    business_name: Optional[str] = None  # For businesses
    is_business: bool
    created_at: datetime = Field(nullable=False, default=datetime.now())
    updated_at: datetime = Field(nullable=False, default=datetime.now())
    reviews: List["Reviews"] = Relationship(back_populates="Vendors")


class Reviews(SQLModel, table=True):
    uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    customer_id: int = Field(foreign_key="Customer.uid")
    car_id: int = Field(foreign_key="Cars.uid")
    rating: int = Field(..., ge=1, le=5)  # Rating between 1 and 5 and ... means this rating can't be empty
    review_text: Optional[str] = None
    created_at: datetime = Field(nullable=False, default_factory=datetime.utcnow)
    updated_at: datetime = Field(nullable=False, default_factory=datetime.utcnow)


    # RELATONSHIPS
customer: "Customers" = Relationship(back_populates="Reviews")
vendor: "Vendors" = Relationship(back_populates="Reviews")
car: Optional["Cars"] = Relationship(back_populates="Reviews")

# it is optional for a customer to give reviews about car he will just give reviews about 
# vendor if he likes the car he will give its review in the same section or if he wants
# explicitly he could do that also
    