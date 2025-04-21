from sqlmodel.ext.asyncio.session import AsyncSession
from src.config import Config

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

    async def login_admin(
            self,
            password: str,
            session: AsyncSession,     
):