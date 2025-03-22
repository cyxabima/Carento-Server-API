from abc import ABC, abstractmethod
from typing import Generic, Optional, Type, TypeVar
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from src import utils
from . import schemas

from src.db.models import BaseUser, Customers, Vendors

# Define a type variable for subclasses of BaseUser
T = TypeVar("T", bound=BaseUser)


#  this is generic class in cpp we called it template
class UserService(ABC, Generic[T]):
    async def get_user_by_email(
        self, email: str, db_model: Type[T], session: AsyncSession
    ):
        statement = select(db_model).where(db_model.email == email)
        result = await session.exec(statement)
        user = result.first()
        return user

    @abstractmethod
    async def sign_up(self, user_data, session: AsyncSession) -> Optional[T]:
        pass

    @abstractmethod
    async def login(self, email: str, password: str, session: AsyncSession):
        pass

    async def log_out(self):
        pass

    async def get_all_users(self):
        pass


class CustomerService(UserService[Customers]):

    async def sign_up(
        self,
        user_data: schemas.CustomerCreateModel,
        session: AsyncSession,
    ):

        customer = await self.get_user_by_email(user_data.email, Customers, session)
        if customer:
            return None

        hashed_password = utils.hash_password(user_data.password)
        user_data.password = hashed_password
        new_customer = Customers(**user_data.model_dump())
        session.add(new_customer)
        await session.commit()
        await session.refresh(new_customer)
        return new_customer

    async def login(self, email: str, password: str, session: AsyncSession):
        customer = await self.get_user_by_email(email, Customers, session)
        if not customer:
            return None

        verify_pass = utils.verify_password(password, customer.password)
        if not verify_pass:
            return None


class VendorService(UserService[Vendors]):
    async def sign_up(
        self,
        user_data: schemas.VendorCreateModel,
        session: AsyncSession,
    ):

        customer = await self.get_user_by_email(user_data.email, Vendors, session)
        if customer:
            return None

        hashed_password = utils.hash_password(user_data.password)
        user_data.password = hashed_password
        new_vendor = Vendors(**user_data.model_dump())
        session.add(new_vendor)
        await session.commit()
        await session.refresh(new_vendor)
        return new_vendor

    async def login(self, email: str, password: str, session: AsyncSession):
        vendor = await self.get_user_by_email(email, Vendors, session)
        if not vendor:
            return None

        verify_pass = utils.verify_password(password, vendor.password)

        if not verify_pass:
            return None
