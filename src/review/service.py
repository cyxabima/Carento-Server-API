from typing import Optional
from sqlmodel import select
from . import schemas
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import BaseUser
from src.db.models import Reviews
import uuid
from src.users.service import CustomerService
from src.vehicles.service import CarService

user_service = CustomerService()
car_service = CarService()


class ReviewService:

    async def get_review_by_id(
        self, review_uid: uuid.UUID, session: AsyncSession
    ) -> Optional[Reviews]:
        """
        Fetches a review by its I.
        """

        statement = select(Reviews).where(
            Reviews.uid == review_uid,
        )
        result = await session.exec(statement)
        return result.first()

    async def has_reviewed(
        self, customer_id: uuid.UUID, car_id: uuid.UUID, session: AsyncSession
    ):
        """
        Checks if a customer has already reviewed a specific car.
        Returns None if the review exists, otherwise reviewed.
        """
        result = await session.exec(
            select(Reviews).where(
                Reviews.customer_id == customer_id, Reviews.car_id == car_id
            )
        )
        reviewed = result.first()
        if reviewed:
            return reviewed

    async def create_review(
        self,
        current_user: BaseUser,
        car_uid: uuid.UUID,
        review: schemas.ReviewCreateModel,
        session: AsyncSession,
    ):
        """
        Creates a new review for a car by customer
        A customer can only review car once.
        """

        # check if customer exists
        customer = await user_service.get_customer_by_email(current_user.email, session)
        if not customer:
            return

        # check  if car exists
        car = await car_service.get_car(car_uid, session)
        if not car:
            return None

        # check if already reviewed

        reviewed = await self.has_reviewed(current_user.uid, car_uid, session)
        if reviewed:
            return

        # Create a new review instance
        review_data = review.model_dump()
        review_data["car_id"] = car_uid
        review_data["customer_id"] = current_user.uid
        new_review = Reviews(**review_data)

        # Add to session and commit
        session.add(new_review)
        await session.commit()
        await session.refresh(new_review)

        return new_review

    async def edit_review(
        self,
        current_user: uuid.UUID,
        review_uid: uuid.UUID,
        updated_review: schemas.ReviewUpdateModel,
        session: AsyncSession,
    ):
        """
        Edit the current review of customer if he has any
        """
        # Check if review exists
        review = await self.get_review_by_id(review_uid, session)

        if not review:
            return

        # Update allowed fields
        if updated_review.rating is not None:
            review.rating = updated_review.rating

        review.review_text = updated_review.review_text

        # Save changes
        await session.commit()
        await session.refresh(review)

        return review

    async def delete_review(self, review_uid: uuid.UUID, session: AsyncSession):
        """
        Delete the review of any customer.
        """
        # Check if review exists
        reviewed = await self.get_review_by_id(review_uid, session)
        if not reviewed:
            return  # will raise an HTTPException

        await session.delete(reviewed)
        await session.commit()
        return {"message": "review deleted successfully"}
