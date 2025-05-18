from fastapi import APIRouter, status, HTTPException, Depends
from src.booking_table.schemas import CreateBookingModel, BookingResponseModel
from src.auth.Dependencies import (
    customer_dependency,
    vendor_dependency,
    get_logged_user,
)
import uuid
from src.db.main import get_async_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import BaseUser
from src.booking_table.service import BookingService

booking_router = APIRouter()
booking_service = BookingService()


@booking_router.post(
    "/create/{car_uid}",
    response_model=BookingResponseModel,
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[customer_dependency],
)
async def create_booking(
    car_uid: uuid.UUID,
    booking_data: CreateBookingModel,
    session: AsyncSession = Depends(get_async_session),
    current_user: BaseUser = Depends(
        get_logged_user
    ),  # Automatically get logged-in user
):
    """
    API Endpoint to allow a customer to book a car.
    A customer can only book a car once if it is not already booked.
    """

    booking = await booking_service.create_booking(
        car_uid,
        booking_data,
        session,
        current_user,
    )

    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Car is already booked or You have less credit.",
        )

    return booking


@booking_router.delete(
    "/delete/{booking_uid}",
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[customer_dependency],
)
async def delete_booking(
    booking_uid: uuid.UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: BaseUser = Depends(
        get_logged_user
    ),  # Automatically get logged-in user
):
    """
    API Endpoint to allow a customer to delete their booking.
    A customer can only delete a booking they created.
    """

    booking = await booking_service.delete_booking(booking_uid, session)

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found or you cannot delete someone else's booking.",
        )

    return booking


@booking_router.get(
    "/get_all",
    response_model=list[BookingResponseModel],  # List of bookings as response model
    status_code=status.HTTP_200_OK,
    dependencies=[vendor_dependency],
)
async def get_vendor_bookings(
    session: AsyncSession = Depends(get_async_session),
    current_user: BaseUser = Depends(
        get_logged_user
    ),  # Automatically get logged-in user
):
    """
    API Endpoint to get all bookings for a vendor.
    Vendors can view all bookings associated with their cars.
    """

    bookings = await booking_service.get_vendor_bookings(current_user.uid, session)

    if not bookings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No bookings found.",
        )

    return bookings


@booking_router.get(
    "/get_customer_bookings",
    response_model=list[BookingResponseModel],  # List of bookings as response model
    status_code=status.HTTP_200_OK,
)
async def get_customer_booking(
    session: AsyncSession = Depends(get_async_session),
    current_user: BaseUser = Depends(
        get_logged_user
    ),  # Automatically get logged-in user
):
    """
    API Endpoint to get all bookings for a Customers.
    Customer can view which car is now at booking for himself.
    """

    booking = await booking_service.get_customer_booking(current_user.uid, session)

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No bookings found.",
        )

    return booking
