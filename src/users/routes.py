from fastapi import APIRouter, Depends
from src.db.main import get_async_session
from sqlmodel.ext.asyncio.session import AsyncSession

from src.users.schemas import CustomerCreateModel
from src.users.service import CustomerService, VendorService

# All End points of Customers
customer_router = APIRouter()
customer_service = CustomerService()


@customer_router.post("/")
async def create_customer(
    customer_data: CustomerCreateModel, db: AsyncSession = Depends(get_async_session)
):
    customer = await customer_service.sign_up(customer_data, db)
    return customer


# All End points of Vendors
vendor_router = APIRouter()
vendor_service = VendorService()
