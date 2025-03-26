from . import schemas
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select
from src.db import models
import uuid

class ReviewService:

    async def create_review(self, 
                            car_uid: uuid.UUID,
                            review: schemas.ReviewCreateModel,
                            session: AsyncSession):
        """
        Creates a new review for a car by customer
        A customer can only review car once.
        """
        # Check if customer exists
        result = await session.execute(select(models.Customers).where(
                                        models.Customers.uid == review.customer_id))
        customer = result.scalars().first()
        if not customer:
            
            return

        # Check if car exists and get its vendor
        result = await session.execute(select(models.Cars).where(
                                         models.Cars.uid == car_uid))
        car = result.scalars().first()
        if not car:
            print('hello')
            return 
        
        # check if already reviewed
        result = await session.execute(select(models.Reviews).where(
                                        models.Reviews.customer_id == review.customer_id,
                                        models.Reviews.car_id == car_uid))
        is_reviewed = result.scalars().first()
        if is_reviewed:
            return 
                                         

        # Create a new review instance((
        review_data= review.model_dump()
        review_data["car_id"] = car_uid  
        new_review = models.Reviews(**review_data)
            

        # Add to session and commit
        session.add(new_review)
        await session.commit()
        await session.refresh(new_review)

        return new_review

    async def edit_review(self,
                            review_uid: str,
                            edited_review: schemas.ReviewUpdateModel,
                            session: AsyncSession):
        """
        Edit the current review of customer if he has any
        """
    # Check if review exists
        result = await session.execute(
            select(models.Reviews).where(models.Reviews.uid == review_uid)
        )
        existing_review = result.scalars().first()
        
        if not existing_review:
            return None  # will raise an HTTPException

        # Update fields that were set in edited_review
        update_review_dict = edited_review.model_dump(exclude_unset=True)
        for key, value in update_review_dict.items():
            setattr(existing_review, key, value)

        await session.commit()
        await session.refresh(existing_review)

        return existing_review
    
    async def delete_review(self,
                             review_uid: str,
                             session: AsyncSession):
        """
        Delete the current review of customer
        """
        # Check if review exists
        result = await session.execute(
            select(models.Reviews).where(models.Reviews.uid == review_uid)
        )
        existing_review = result.scalars().first()
        
        if not existing_review:
            return None  # will raise an HTTPException
        await session.delete(existing_review)
        await session.commit()
        return {"message": "review deleted successfully"}