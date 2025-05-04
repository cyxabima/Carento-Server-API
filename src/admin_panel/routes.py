from fastapi import APIRouter, status, HTTPException, Depends
from typing import List

from src.auth.Dependencies import (
    admin_dependency,
    get_logged_user,
)
import uuid
from src.db.main import get_async_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.booking_table.service import BookingService
from src.config import Config
from src.admin_panel.service import AdminService
from src.vehicles.service import CarService
from src.users.service import CustomerService, VendorService
from src.admin_panel.schemas import (
    AdminGetModel,
    AdminCarGetModel,
    BookingGetModel,
    CustomerGetModel,
    VendorGetModel,
    UserDeleteModel,
)
from pydantic import EmailStr

admin_router = APIRouter()

booking_service = BookingService()
admin_service = AdminService()
car_service = CarService()
customer_service = CustomerService()
vendor_service = VendorService()

admin_password = Config.ADMIN_PANEL_PASSWORD


# ---------------------- ADMIN LOGIN ----------------------
@admin_router.post(
    "/login/{password}",
    status_code=status.HTTP_202_ACCEPTED,
    # dependencies=[admin_dependency],
    response_model=AdminGetModel,
)
async def login_admin(
    password: str,
    session: AsyncSession = Depends(get_async_session),
):

    admin = await admin_service.login_admin(password, session)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin password",
        )
    return admin


# ---------------------- BOOKING ROUTES ----------------------
@admin_router.delete(
    "/delete-booking/{booking_uid}",
    status_code=status.HTTP_202_ACCEPTED,
    # dependencies=[admin_dependency],
)
async def delete_booking(
    booking_uid: uuid.UUID,
    session: AsyncSession = Depends(get_async_session),
):
    """
    API Endpoint to allow admin to delete any booking.
    An admin can delete booking of any customer.
    """

    booking = await booking_service.delete_booking(booking_uid, session)

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found.",
        )

    return booking


@admin_router.get(
    "/get_all",
    response_model=list[BookingGetModel],  # List of bookings as response model
    status_code=status.HTTP_200_OK,
    # dependencies=[admin_dependency],
)
async def get_all_bookings(
    session: AsyncSession = Depends(get_async_session),
):
    """
    API Endpoint to get all bookings for all cars.
    Admin can view all booked cars.
    """

    bookings = await booking_service.get_all_bookings(session)

    if not bookings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No bookings found.",
        )

    return bookings


# ---------------------- REVIEW ROUTES ----------------------
@admin_router.delete(
    "/delete_review/{review_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    # dependencies=[admin_dependency],
)
async def delete_review(
    review_uid: uuid.UUID,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Allows admin to delete any review.
    """

    review = await admin_service.delete_review(review_uid, session)

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found.",
        )
    return {
        "content": "deleted successfully",
        "status_code": status.HTTP_204_NO_CONTENT,
    }


# ---------------------- VEHICLE ROUTES ----------------------
@admin_router.get(
    "/cars",
    response_model=List[AdminCarGetModel]
)
async def get_all_cars(
    db: AsyncSession = Depends(get_async_session),
):
    cars = await admin_service.get_all_cars(db)
    return cars


@admin_router.get("/cars/{car_uid}", response_model=AdminCarGetModel)
async def get_car(
    car_uid: uuid.UUID,
    db: AsyncSession = Depends(get_async_session),
):
    car = await car_service.get_car(car_uid, db)
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "car with this uid is not found"},
        )
    return car


@admin_router.delete(
    "/cars/{car_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_car(car_uid: uuid.UUID, db: AsyncSession = Depends(get_async_session)):
    car = await car_service.delete_car(car_uid, db)

    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "car with this uid is not found"},
        )

    return car


# ---------------------- CUSTOMERS ROUTES ----------------------
@admin_router.get(
    "/customers",
    response_model=List[CustomerGetModel],
)
async def get_all_customers(session: AsyncSession = Depends(get_async_session)):

    customers = await admin_service.get_all_customers(session)
    return customers


@admin_router.get(
    "/customer",
    response_model=CustomerGetModel,
)
async def get_customer_by_email(email: EmailStr, session: AsyncSession = Depends(get_async_session)):

    customer = await customer_service.get_customer_by_email(email, session)
    return customer


@admin_router.delete(
    "/customers",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_customers(
    user_email: EmailStr,
    session: AsyncSession = Depends(get_async_session),
):

    result = await admin_service.delete_account(user_email, session)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or person not found.",
        )
    return {"message": "Account deleted successfully"}


# ---------------------- VENDOR FUNCTIONS ----------------------
@admin_router.get(
    "/vendors",
    response_model=List[VendorGetModel],
)
async def get_all_vendors(session: AsyncSession = Depends(get_async_session)):
    vendors = await admin_service.get_all_vendors(session)
    return vendors


@admin_router.get(
    "/vendor",
    response_model=VendorGetModel,
)
async def get_vendor_by_email(email: EmailStr, session: AsyncSession = Depends(get_async_session)):

    vendor = await vendor_service.get_vendor_by_email(email, session)
    return vendor


@admin_router.delete(
    "/vendors",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_customers(
    user_email: EmailStr,
    session: AsyncSession = Depends(get_async_session),
):

    result = await admin_service.delete_account(user_email, session)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or person not found.",
        )
    return {"message": "Account deleted successfully"}
