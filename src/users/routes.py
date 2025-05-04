from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.Dependencies import (
    customer_dependency,
    get_logged_user,
    vendor_dependency,
)

from src.db.main import get_async_session
from src.db.models import BaseUser
from .service import CustomerService, VendorService
from . import schemas

customer_router = APIRouter()
vendor_router = APIRouter()

customer_service = CustomerService()
vendor_service = VendorService()


@customer_router.post(
    "/signup",
    response_model=schemas.CustomerResponseModel,
    status_code=status.HTTP_201_CREATED,
)
async def customer_signup(
    user_data: schemas.CustomerCreateModel,
    session: AsyncSession = Depends(get_async_session),
):

    customer = await customer_service.sign_up(user_data, session)

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customer already exists.",
        )
    return customer


@customer_router.post("/login", status_code=status.HTTP_202_ACCEPTED)
async def customer_login(
    customer_credentials: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session),
):

    customer_token = await customer_service.login(
        customer_credentials.username, customer_credentials.password, session
    )

    if not customer_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
        )

    return customer_token


@customer_router.delete(
    "/delete",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[customer_dependency],
)
async def customer_delete_account(
    user_data: schemas.UserDeleteModel,
    session: AsyncSession = Depends(get_async_session),
):

    result = await customer_service.delete_account(user_data, session)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials or customer not found.",
        )
    return {"message": "Account deleted successfully"}


@vendor_router.post(
    "/signup",
    response_model=schemas.VendorResponseModel,
    status_code=status.HTTP_201_CREATED,
)
async def vendor_signup(
    user_data: schemas.VendorCreateModel,
    session: AsyncSession = Depends(get_async_session),
):

    vendor = await vendor_service.sign_up(user_data, session)

    if vendor is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vendor email or Business name already exists.",
        )
    return vendor


@vendor_router.post("/login", status_code=status.HTTP_202_ACCEPTED)
async def vendor_login(
    vendor_credentials: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session),
):

    vendor_token = await vendor_service.login(
        vendor_credentials.username, vendor_credentials.password, session
    )  # remember username is email in our system

    if not vendor_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
        )
    return vendor_token


@vendor_router.delete(
    "/delete", status_code=status.HTTP_204_NO_CONTENT, dependencies=[vendor_dependency]
)
async def vendor_delete_account(
    user_data: schemas.UserDeleteModel,
    session: AsyncSession = Depends(get_async_session),
):

    result = await vendor_service.delete_account(user_data, session)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials or vendor not found.",
        )
    # return {"message": "Account deleted successfully"}


@vendor_router.get("/me", response_model=schemas.VendorResponseModel)
async def get_logged_vendor(
    currentUser: BaseUser = Depends(get_logged_user),
    session: AsyncSession = Depends(get_async_session),
):

    me = await vendor_service.get_vendor_by_email(currentUser.email, session)

    if not me:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vendor Not Found"
        )

    return me
