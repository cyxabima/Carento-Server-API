from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import *
from src.db.main import get_async_session
from .service import ReviewService

review_router = APIRouter()
review_service = ReviewService()

@review_router.post("/reviews/{car_uid}",
                    response_model=ReviewResponseModel,
                    status_code=status.HTTP_201_CREATED)
async def post_review(car_uid: uuid.UUID,
                        review: ReviewCreateModel,
                       session: AsyncSession = Depends(get_async_session)):
    reviewed = await review_service.create_review(car_uid, review, session)

    if not reviewed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="review already exists.",   #there could be more appropriate msg, would add in frontend 
        )
    return reviewed

@review_router.patch("/update_review",
                    response_model=ReviewResponseModel,
                    status_code=status.HTTP_200_OK)
async def edit_review():
    pass


@review_router.delete("/delete_review/{}",
                      status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(review_uid):
    pass