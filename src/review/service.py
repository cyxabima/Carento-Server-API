from sqlmodel import select
from . import schemas
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.models import Customers, Cars, Reviews
import uuid


class ReviewService:

    async def create_review(
        self,
        car_uid: uuid.UUID,
        review: schemas.ReviewCreateModel,
        session: AsyncSession,
    ):
        """
        Creates a new review for a car by customer
        A customer can only review car once.
        """

        # Check if customer exists
        customer_statement = select(Customers).where(
            Customers.uid == review.customer_id
        )
        result = await session.exec(customer_statement)
        customer = result.first()
        if not customer:
            return

        # Check if car exists and get its vendor
        car_statement = select(Cars).where(Cars.uid == car_uid)
        result = await session.exec(car_statement)
        car = result.first()
        if not car:
            print("hello")
            return

        # check if already reviewed
        review_exist_statement = select(Reviews).where(
            Reviews.customer_id == review.customer_id,
            Reviews.car_id == car_uid,
        )
        result = await session.exec(review_exist_statement)
        is_reviewed = result.first()

        if is_reviewed:
            return

        # Create a new review instance((
        review_data = review.model_dump()
        review_data["car_id"] = car_uid
        new_review = Reviews(**review_data)

        # Add to session and commit
        session.add(new_review)
        await session.commit()
        await session.refresh(new_review)

        return new_review

    async def edit_review(
        self,
        review_uid: str,
        edited_review: schemas.ReviewUpdateModel,
        session: AsyncSession,
    ):
        """
        Edit the current review of customer if he has any
        """
        # Check if review exists
        get_review_statement = select(Reviews).where(Reviews.uid == review_uid)
        result = await session.exec(get_review_statement)
        existing_review = result.first()

        if not existing_review:
            return None  # will raise an HTTPException

        # Update fields that were set in edited_review
        update_review_dict = edited_review.model_dump(exclude_unset=True)
        for key, value in update_review_dict.items():
            setattr(existing_review, key, value)

        await session.commit()
        await session.refresh(existing_review)

        return existing_review

    async def delete_review(self, review_uid: str, session: AsyncSession):
        """
        Delete the current review of customer
        """
        # Check if review exists
        statement = select(Reviews).where(Reviews.uid == review_uid)
        result = await session.exec(statement)
        existing_review = result.first()

        if not existing_review:
            return None  # will raise an HTTPException

        await session.delete(existing_review)
        await session.commit()
        return {"message": "review deleted successfully"}
