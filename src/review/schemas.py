from pydantic import Field, BaseModel
from typing import Optional
from datetime import datetime
import uuid

from src.db.models import Customers


class ReviewCreateModel(BaseModel):
    rating: int = Field(..., ge=1, le=5)  # Ensures rating is between 1-5
    review_text: Optional[str] = None


class ReviewUpdateModel(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    review_text: Optional[str] = None


class ReviewResponseModel(ReviewCreateModel):
    uid: uuid.UUID
    customer: Customers
    created_at: datetime
    updated_at: datetime
