from pydantic import Field
from typing import Optional
from sqlmodel import SQLModel
from datetime import datetime
import uuid


class ReviewCreateModel(SQLModel):
    rating: int = Field(..., ge=1, le=5)  # Ensures rating is between 1-5
    review_text: Optional[str] = None

class ReviewUpdateModel(SQLModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    review_text: Optional[str] = None

class ReviewResponseModel(ReviewCreateModel):
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime
