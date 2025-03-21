from abc import ABC, abstractmethod
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException
from sqlmodel import select

from src.db.models import Users
from src import utils
from . import schemas

class UserService(ABC):
    @abstractmethod
    async def sign_up(self, 
                    user_data: schemas.UserCreateModel,
                    session: AsyncSession):
        hashed_password = utils.hash_password(new_user.password)
        new_user.password = hashed_password
        new_user = Users(**user_data.model_dump())
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

    @abstractmethod
    async def login(self, 
                    email: str, 
                    password: str, 
                    session: AsyncSession):        
        query = select(Users).where(Users.email == email)
        result = await session.execute(query)
        user = result.scalars().first()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        verify_pass = utils.verify_password (password, user.hashed_password)
        if not verify_pass:
            raise HTTPException(status_code=401, detail="Invalid email or password")
   
    @abstractmethod
    async def log_out(self):
        pass


class OwnerService(UserService):
    pass


class RenterService(UserService):
    pass
