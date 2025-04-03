from fastapi import APIRouter, status, HTTPException, Depends
from . schemas import CreateBookingModel, BookingResponseModel
from src.auth.Dependencies import customer_dependency, vendor_dependency, get_logged_user 
import uuid
from src.db.main import get_async_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import BaseUser
from .service import BookingService

booking_router = APIRouter()
booking_service = BookingService()


@booking_router.post(
      "/create/{car_uid}",
      response_model=BookingResponseModel,
      status_code= status.HTTP_202_ACCEPTED,
      dependencies= [customer_dependency],
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
    A customer can only book a car once iff it is not already booked.
    """

    booking = await booking_service.create_booking(
        car_uid, booking_data, session, current_user,
    )

    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Car is already booked or invalid request.",
        )
    
    return booking

@booking_router.delete(
    "/delete", response_model=BookingResponseModel,
      status_code= status.HTTP_202_ACCEPTED, dependencies= [customer_dependency]
      )
async def delete_booking(

):
    pass


@booking_router.get(
    "/get_all", response_model=BookingResponseModel,
      status_code= status.HTTP_202_ACCEPTED, dependencies= [vendor_dependency]
      )
async def get_all_bookings(

):
    pass