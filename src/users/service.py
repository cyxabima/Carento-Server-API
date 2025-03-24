from abc import ABC, abstractmethod
from typing import Generic, Optional, Sequence, Type, TypeVar
# import uuid
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from src import utils
from src.auth.oauth2 import AuthService
from . import schemas

from src.db.models import BaseUser, Customers, Vendors

# Type[T] represent class type and T represent object type
# Define a type variable for subclasses of BaseUser
T = TypeVar("T", bound=BaseUser)


#  this is generic class in cpp we called it template
class UserService(ABC, Generic[T]):
    auth_service = AuthService()

    # get all users method
    async def get_all_users(
        self, db_model: Type[T], session: AsyncSession
    ) -> Sequence[T]:
        statement = select(db_model)
        users = await session.exec(statement)
        return users.all()

    # get user by email method
    async def get_user_by_email(
        self, email: str, db_model: Type[T], session: AsyncSession
    ) -> Optional[T]:
        statement = select(db_model).where(db_model.email == email)
        result = await session.exec(statement)
        user = result.first()
        return user

    # abstract methods for sign up login and delete account
    @abstractmethod
    async def sign_up(self, user_data, session: AsyncSession) -> Optional[T]:
        pass

    @abstractmethod
    async def login(
        self, email: str, password: str, session: AsyncSession
    ) -> Optional[str]:
        pass

    @abstractmethod
    async def delete_account(
        self, user_data: schemas.UserDeleteModel, session: AsyncSession
    ) -> Optional[int]:
        pass

    #  Incomplete method for logout
    async def log_out(self):
        pass


class CustomerService(UserService[Customers]):
    #  get all customer
    async def get_all_customers(self, session: AsyncSession):
        all_customers = await self.get_all_users(Customers, session)
        return all_customers

    # get customer by email
    async def get_customer_by_email(self, email, session: AsyncSession):
        customer = await self.get_user_by_email(email, Customers, session)
        return customer

    # signup for customer
    async def sign_up(
        self,
        user_data: schemas.CustomerCreateModel,
        session: AsyncSession,
    ):

        customer = await self.get_customer_by_email(user_data.email, session)
        if customer:
            return

        hashed_password = utils.hash_password(user_data.password)
        user_data.password = hashed_password
        new_customer = Customers(**user_data.model_dump())
        session.add(new_customer)
        await session.commit()
        await session.refresh(new_customer)
        return new_customer

    # login for customer
    async def login(self, email: str, password: str, session: AsyncSession):
        customer = await self.get_user_by_email(email, Customers, session)
        if not customer:
            return

        verify_pass = utils.verify_password(password, customer.password)
        if not verify_pass:
            return
        token_data = schemas.TokenDataModel(email=email, role="Customer")
        token = self.auth_service.create_access_token(data=token_data.model_dump())

        return token

    # delete customer account
    async def delete_account(
        self, user_data: schemas.UserDeleteModel, session: AsyncSession
    ):
        customer = await self.get_customer_by_email(user_data.email, session)
        if not customer:
            return

        if not utils.verify_password(user_data.password, customer.password):
            return

        await session.delete(customer)
        await session.commit()
        return 200


class VendorService(UserService[Vendors]):

    #  get all vendors
    async def get_all_vendors(self, session: AsyncSession):
        all_vendors = await self.get_all_users(Vendors, session)
        return all_vendors

    # get vendor by email
    async def get_vendor_by_email(self, email, session: AsyncSession):
        vendor = await self.get_user_by_email(email, Vendors, session)
        return vendor

    # signup for vendor
    async def sign_up(
        self,
        user_data: schemas.VendorCreateModel,
        session: AsyncSession,
    ):

        vendor = await self.get_vendor_by_email(user_data.email, session)
        if vendor:
            return

        if user_data.business_name:
            statement = select(Vendors).where(
                Vendors.business_name == user_data.business_name
            )
            find_business = await session.exec(statement)
            business = find_business.first()
            if business:
                return

        hashed_password = utils.hash_password(user_data.password)
        user_data.password = hashed_password
        new_vendor = Vendors(**user_data.model_dump())
        session.add(new_vendor)
        await session.commit()
        await session.refresh(new_vendor)
        return new_vendor

    # login for vendor
    async def login(self, email: str, password: str, session: AsyncSession):
        vendor = await self.get_vendor_by_email(email, session)
        if not vendor:
            return

        verify_pass = utils.verify_password(password, vendor.password)

        if not verify_pass:
            return

        token_data = schemas.TokenDataModel(email=email, role="Vendor")
        token = self.auth_service.create_access_token(data=token_data.model_dump())

        return token

    # delete vendor account
    async def delete_account(
        self, user_data: schemas.UserDeleteModel, session: AsyncSession
    ):
        vendor = await self.get_vendor_by_email(user_data.email, session)
        if not vendor:
            return

        if not utils.verify_password(user_data.password, vendor.password):
            return

        await session.delete(vendor)
        await session.commit()
        return 200
