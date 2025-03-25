from pydantic import Field, BaseModel
from typing import Optional
from sqlmodel import SQLModel


class ReviewCreateModel(SQLModel):
    customer_id: int
    car_id: int
    rating: int = Field(..., ge=1, le=5)  # Ensures rating is between 1-5
    review_text: Optional[str] = None
    
class ReviewUpdateModel(SQLModel):
    rating: Optional [int] = Field (None, ge=1, le=5)
    review_text: Optional[str] = None 

# class ReviewDeleteModel(SQLModel):
