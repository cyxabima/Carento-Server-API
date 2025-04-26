from sqlmodel.ext.asyncio.session import AsyncSession
from src.config import Config
import uuid
from src.db.models import Reviews, Cars
from sqlmodel import select, desc
from src.booking_table.service import BookingService
from src.users.service import CustomerService
from src.vehicles.service import VehicleService
from typing import Tuple, Sequence

admin_password = Config.ADMIN_PANEL_PASSWORD
admin_name = Config.ADMIN_NAME


class AdminService(CustomerService, VehicleService):
    async def login_admin(
        self,
        password: str,
        session: AsyncSession,
    ):

        if password != admin_password:
            return

        return {"message": f"Welcome {admin_name} to Admin Panel!"}

    async def delete_review(
        self,
        review_uid: uuid.UUID,
        session: AsyncSession,
    ):
        """
        Delete the any review of any customer
        """
        statement = select(Reviews).where(
            Reviews.uid == review_uid,
        )
        result = await session.exec(statement).first()
        if not result:
            return
        await session.delete(result)
        await session.commit()
        return {"message": "review deleted successfully"}

    async def get_all_cars(self, session: AsyncSession) -> tuple[Sequence[Cars], int]:
        cars = await super().get_all_cars(session)  # call parent function
        total_cars = len(cars)
        return cars, total_cars

    async def get_all_customers(self, session: AsyncSession):
        all_customers = await super().get_all_users(Customers, session)
        total_customers = len(all_customers)
        return all_customers, total_customers
