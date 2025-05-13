from src.wallet.schemas import WalletGetModel, WalletAddModel
from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.db.models import Wallet
import uuid


class WalletService:

    async def get_my_wallet(
        self, customer_uid: uuid.UUID, session: AsyncSession
    ) -> Optional[WalletGetModel]:
        stmt = select(Wallet).where(
            Wallet.customer_id == customer_uid,
        )
        result = await session.exec(stmt)
        wallet = result.first()

        if wallet is None:
            return

        return wallet

    async def add_in_wallet(
        self, credit: float, customer_uid: uuid.UUID, session: AsyncSession
    ) -> None:

        wallet = await self.get_my_wallet(customer_uid, session)

        if wallet is None:
            return

        wallet += credit

        session.add(wallet)
        await session.commit()

        return {"message": f"{credit} dollars added to your account successfully"}
