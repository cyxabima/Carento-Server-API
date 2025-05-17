from typing import Optional
from src.db.models import Cars, Booking, Wallet
from src.db.models import BaseUser
from sqlmodel import select
from src.booking_table.schemas import CreateBookingModel
from src.vehicles.service import CarService
from src.wallet.service import WalletService
import uuid
from sqlmodel.ext.asyncio.session import AsyncSession


class BookingService:

    def __init__(self) -> None:
        self.car_service: CarService = CarService()
        self.wallet_service: WalletService = WalletService()

    # Get booking by UID
    async def get_booking_by_uid(self, booking_uid: uuid.UUID, session: AsyncSession):
        statement = select(Booking).where(Booking.uid == booking_uid)
        result = await session.exec(statement)
        booking = result.first()

        if not booking:
            print("Booking not found")
            return None

        return booking

    # Check if the car is available
    async def is_car_available(self, car_uid: uuid.UUID, session: AsyncSession):
        # Check if car exists
        car = await self.car_service.get_car(car_uid, session)

        if not car:
            print("Car not found")
            return False

        if car.is_booked:
            print("Car is already booked")
            return False

        return True

    # Create a booking
    async def create_booking(
        self,
        car_uid: uuid.UUID,
        booking: CreateBookingModel,
        session: AsyncSession,
        current_user: BaseUser,
    ):

        # Check if car is available
        is_available = await self.is_car_available(car_uid, session)

        if not is_available:
            print("Car is not available")
            return None

        car = await self.car_service.get_car(car_uid, session)
        if not car:
            return
        car.is_booked = True
        price = car.price_per_day

        # Fetch wallet
        wallet: Optional[Wallet] = await self.wallet_service.get_my_wallet(
            current_user.uid, session
        )

        if wallet is None:
            return

        # Deduct from wallet
        wallet -= price
        session.add(wallet)

        booking_data = booking.model_dump()
        booking_data["car_id"] = car_uid
        booking_data["customer_id"] = current_user.uid
        booking_data["total_price"] = car.price_per_day
        new_booking = Booking(**booking_data)
        session.add(new_booking)
        await session.commit()
        await session.refresh(new_booking)

        return new_booking

    # Delete a booking
    async def delete_booking(self, booking_uid: uuid.UUID, session: AsyncSession):
        booking = await self.get_booking_by_uid(booking_uid, session)
        if not booking:
            print("Booking not found")
            return None

        # set the car back to available
        result = await session.exec(select(Cars).where(Cars.uid == booking.car_id))
        car = result.first()
        if car:
            car.is_booked = False
            await session.commit()

        # in this logic it might be difficult to use get_car  because
        # delete_booking takes only one argument so we have two options
        # either we take car_uid here or we have to take that as a url in end point
        # so it is better to define logic explicitly imo

        # Delete the booking
        await session.delete(booking)
        await session.commit()
        print("Booking successfully deleted")
        return {"message": "Booking successfully deleted"}

    # Get all bookings
    async def get_my_bookings(self, vendor_uid: uuid.UUID, session: AsyncSession):
        statement = (
            select(Booking)
            .join(Cars, Booking.car_id == Cars.uid)
            .where(Cars.vendor_id == vendor_uid)
        )
        result = await session.exec(statement)
        bookings = result.all()

        if not bookings:
            print("No bookings found")
            return None

        return bookings
