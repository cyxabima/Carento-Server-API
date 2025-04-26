from sqlmodel.ext.asyncio.session import AsyncSession
from src.config import Config
import uuid
from src.db.models import Reviews
from sqlmodel import select

admin_password = Config.ADMIN_PANEL_PASSWORD
admin_name = Config.ADMIN_NAME
class AdminService:
    async def login_admin(
            self,
            password: str,
            session: AsyncSession,     
):

        if password != admin_password:
            return

        return {"message": f"Welcome {admin_name} to Admin Panel!"}

    async def delete_review(
            self,
            review_uid:uuid.UUID,
            session: AsyncSession,     
):
        """
        Delete the any review of any customer
        """
        statement = select(Reviews).where(
            Reviews.uid == review_uid,     
        )
        result = await session.exec(statement).first()
        if not result:
            return        
        await session.delete(result)
        await session.commit()
        return {"message": "review deleted successfully"}