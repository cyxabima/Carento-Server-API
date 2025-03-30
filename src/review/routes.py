import uuid
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import ReviewCreateModel, ReviewResponseModel, ReviewUpdateModel
from src.db.main import get_async_session
from .service import ReviewService
from src.auth.Dependencies import review_dependency, get_logged_user
from src.db.models import BaseUser


review_router = APIRouter()
review_service = ReviewService()

<<<<<<< HEAD

async def get_review_by_id(
    review_uid: uuid.UUID, customer_id: uuid.UUID, session: AsyncSession
) -> Optional[Reviews]:
    """
    Fetches a review by its ID and ensures that the given customer is the author.
    """
    statement = select(Reviews).where(
        Reviews.uid == review_uid,
        Reviews.customer_id
        == customer_id,  # Ensures only the author(customer) can fetch
    )
    result = await session.exec(statement)
    return result.first()
=======
>>>>>>> test


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
<<<<<<< HEAD
=======
    dependencies=[review_dependency],
>>>>>>> test
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

<<<<<<< HEAD
    review = await get_review_by_id(review_uid, current_user.uid, session)

=======
>>>>>>> test
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found or you are not authorized to update it.",
        )

    return review


@review_router.delete(
<<<<<<< HEAD
    "/delete_review/{review_uid}", status_code=status.HTTP_204_NO_CONTENT
=======
    "/delete_review/{review_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[review_dependency],
>>>>>>> test
)
async def delete_review(
    review_uid: uuid.UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: BaseUser = Depends(get_logged_user),
):
    """
    Allows a customer to delete their own review.
    """

<<<<<<< HEAD
    review = await get_review_by_id(review_uid, current_user.uid, session)
=======
    review = await review_service.delete_review(review_uid, current_user.uid, session)
>>>>>>> test

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found or you are not authorized to delete it.",
        )
    return Response(
        content="deleted successfully", status_code=status.HTTP_204_NO_CONTENT
    )


# /* up till here the main functionality has been done additional functionality
# just like all reviews for specific vendor and all the reviews of specific customer*/
