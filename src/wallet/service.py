from typing import Dict, Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.db.models import Wallet
import uuid


class WalletService:

    async def get_customer_wallet(
        self, customer_uid: uuid.UUID, session: AsyncSession
    ) -> Optional[Wallet]:
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
    ) -> Optional[Dict[str, str]]:

        wallet = await self.get_customer_wallet(customer_uid, session)

        if wallet is None:
            return

        wallet += credit

        session.add(wallet)
        await session.commit()

        return {"message": f"{credit} credits added to your account successfully"}

    async def get_vendor_wallet(
        self, vendor_uid: uuid.UUID, session: AsyncSession
    ) -> Optional[Wallet]:

        statement = select(Wallet).where(
            Wallet.vendor_id == vendor_uid,
        )
        result = await session.exec(statement)
        wallet = result.first()

        if wallet is None:
            return

        return wallet
