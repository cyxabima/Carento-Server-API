from fastapi import APIRouter, status, HTTPException, Depends
from src.booking_table.schemas import BookingResponseModel
from src.auth.Dependencies import (
    admin_dependency,
    get_logged_user,
)
import uuid
from src.db.main import get_async_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import BaseUser
from src.booking_table.service import BookingService
from src.config import Config
from src.review.service import ReviewService
from src.admin_panel.service import AdminService
from src.admin_panel.schemas import AdminGetModel

admin_router = APIRouter()
booking_service = BookingService()
admin_service = AdminService()

admin_password = Config.ADMIN_PANEL_PASSWORD

@admin_router.post(
    "/login/{password}",
    status_code=status.HTTP_202_ACCEPTED,
    # dependencies=[admin_dependency],
    # response_model=AdminGetModel,
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
    response_model=list[BookingResponseModel],  # List of bookings as response model
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


@review_router.delete(
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

    review = await review_service.delete_review(review_uid, current_user.uid, session)

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found.",
        )
    return Response(
        content="deleted successfully", status_code=status.HTTP_204_NO_CONTENT
    )
