from pydantic import Field
from typing import Optional
from sqlmodel import SQLModel
from datetime import datetime
import uuid

class ReviewCreateModel(SQLModel):
    customer_id: uuid.UUID
    car_id: Optional[uuid.UUID] = None # no matter we would pass it in body or not just we have to give in the url    
    rating: int = Field(..., ge=1, le=5)  # Ensures rating is between 1-5
    review_text: Optional[str] = None
    
class ReviewUpdateModel(SQLModel):
    rating: Optional [int] = Field (None, ge=1, le=5)
    review_text: Optional[str] = None 

# class ReviewDeleteModel(SQLModel):
#     review_uid: str 

class ReviewResponseModel(ReviewCreateModel):
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime