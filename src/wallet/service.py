from src.wallet.schemas import WalletGetModel, WalletAddModel
from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.db.models import Wallet
import uuid


class WalletService:
    
    async def add_in_wallet(self, wallet_id: uuid.UUID, payload: WalletAddModel, session: AsyncSession) -> None:
        stmt = select(Wallet).where(
            Wallet.customer_id == payload.customer_uid,
            Wallet.uid == wallet_id
        )
        result = await self.session.exec(stmt)
        wallet = result.first()

        if wallet is None:
            return  # Or raise an exception if needed

        wallet += payload.credit  # Calls __iadd__ in your Wallet model

        await self.session.add(wallet)
        await self.session.commit()
        
        

    async def get_my_wallet(self) -> Optional[WalletGetModel]:
        pass
