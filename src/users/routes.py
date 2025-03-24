from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_async_session
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
    email: str, password: str, session: AsyncSession = Depends(get_async_session)
):

    customer = await customer_service.login(email, password, session)

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
        )
    return {"message": "Login successful"}


@customer_router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
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
    email: str, password: str, session: AsyncSession = Depends(get_async_session)
):

    vendor = await vendor_service.login(email, password, session)

    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
        )
    return {"message": "Login successful"}


@vendor_router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
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
