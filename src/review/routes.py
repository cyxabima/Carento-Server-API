import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import ReviewCreateModel, ReviewResponseModel, ReviewUpdateModel
from src.db.main import get_async_session
from .service import ReviewService
from src.auth.Dependencies import review_dependency, get_logged_user
from src.db.models import BaseUser


review_router = APIRouter()
review_service = ReviewService()


@review_router.post(
    "/create/{car_uid}",
    response_model=ReviewResponseModel,
    status_code=status.HTTP_201_CREATED,
    dependencies=[review_dependency],
)
async def post_review(
    car_uid: uuid.UUID,
    review: ReviewCreateModel,
    session: AsyncSession = Depends(get_async_session),
    current_user: BaseUser = Depends(
        get_logged_user
    ),  # Automatically get logged-in user
):
    """
    API Endpoint to allow a customer to post a review for a car.
    A customer can only review a car once.
    """

    # Call the service function
    reviewed = await review_service.create_review(
        current_user, car_uid, review, session
    )

    if reviewed is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Review already exists or invalid request.",
        )

    return reviewed


@review_router.patch(
    "/update_review/{review_uid}",
    response_model=ReviewResponseModel,
    status_code=status.HTTP_200_OK,
    dependencies=[review_dependency],
)
async def edit_review(
    review_uid: uuid.UUID,
    updated_review: ReviewUpdateModel,
    session: AsyncSession = Depends(get_async_session),
    current_user: BaseUser = Depends(get_logged_user),
):
    """
    Allows a customer to update their existing review.
    Both review text and rating can be updated.
    """
    review = await review_service.edit_review(
        current_user.uid, review_uid, updated_review, session
    )

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found or you are not authorized to update it.",
        )

    return review


@review_router.delete(
    "/delete_review/{review_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[review_dependency],
)
async def delete_review(
    review_uid: uuid.UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: BaseUser = Depends(get_logged_user),
):
    """
    Allows a customer to delete their own review.
    """

    review = await review_service.get_review_by_id(review_uid, session)

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found.",
        )

    if current_user.uid != review.customer_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot delete someone else's review.",
        )

    await review_service.delete_review(review_uid, session)

    return {
        "content": "Deleted successfully",
        "status_code": status.HTTP_204_NO_CONTENT,
    }
