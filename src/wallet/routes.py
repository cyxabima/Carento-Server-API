from fastapi import APIRouter, Depends, HTTPException, status
from src.auth.Dependencies import customer_dependency, get_logged_user
from src.db.main import get_async_session
from src.db.models import BaseUser
from src.wallet.schemas import WalletAddModel
from src.wallet.service import WalletService
from sqlmodel.ext.asyncio.session import AsyncSession

wallet_router = APIRouter()
wallet_service = WalletService()


@wallet_router.patch(
    "/add-in-wallet",  # response_model=WalletGetModel,
    dependencies=[customer_dependency],
)
async def add_in_wallet(
    payload: WalletAddModel,
    current_user: BaseUser = Depends(get_logged_user),
    session: AsyncSession = Depends(get_async_session),
):
    my_wallet = await wallet_service.add_in_wallet(
        payload.credit, current_user.uid, session
    )

    if not my_wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="wallet not found",
        )
    return my_wallet


@wallet_router.get(
    "/my-wallet",
    # response_model=WalletGetModel,
    dependencies=[customer_dependency],
)
async def get_my_wallet(
    current_user: BaseUser = Depends(get_logged_user),
    session: AsyncSession = Depends(get_async_session),
):
    my_wallet = await wallet_service.get_my_wallet(current_user.uid, session)
    if not my_wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="wallet not found",
        )
    return {"current_balance": my_wallet.credit}


# we have an option to return on the response model of wallet but it
# would give the field name which might be inappropriate so i
# explicitly returned the dicts
