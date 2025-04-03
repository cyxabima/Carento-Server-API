from src.db.models import Cars, Booking
from src.db.models import BaseUser
from sqlmodel import Session, select
from src.booking_table.schemas import BookingResponseModel, BookingStatus, CreateBookingModel
from datetime import datetime
from src.vehicles.service import CarService
import uuid
from sqlmodel.ext.asyncio.session import AsyncSession
from src.review.service import user_service

car_service = CarService()

class BookingService:

    async def is_car_available(
            self, 
            car_id: uuid.UUID,
            session: AsyncSession
            ):
        statement = select(Cars).where(
            Cars.uid == car_id
        )
        result = await session.exec(statement)
        car = result.first()
        
        if not car:
            print("uper waly me car nh mili")
            return False  
        
        if car.is_booked == True:
            print('aalready booked he')
            return False
        
        return True  

    async def create_booking(
            self, 
            car_uid: uuid.UUID,
            booking: CreateBookingModel,
            session: AsyncSession,
            current_user: BaseUser,
            ):
        
        # Check if customer exists
        customer = await user_service.get_customer_by_email(
            current_user.email, session
        )
        if not customer:
            print('customer nh he')
            return None
        
        # Check if car exists
        car = await car_service.get_car(car_uid, session)
        if not car:
            print('car nh he')
            return None
        
        # Check if car is available
        is_available = await self.is_car_available(
            car_uid, session
        )
        
        if not is_available:  
            print('available nh he')
            return None
        
        booking_data = booking.model_dump()
        booking_data["car_id"] = car_uid
        booking_data["customer_id"] = current_user.uid
        new_booking = Booking(**booking_data)
        session.add(new_booking)
        
        result = await session.exec(select(Cars).where(Cars.uid == car_uid))
        car = result.first()
        car.is_booked = True  # Mark car as booked
        
        await session.commit() 
        await session.refresh(new_booking)
        return new_booking

