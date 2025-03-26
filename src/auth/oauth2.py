from typing import List, Optional
import uuid
import jwt
from datetime import timedelta, datetime, timezone

from sqlmodel import select
from src.config import Config
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_async_session
from src.db.models import Customers, Vendors

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthService:
    algorithm = Config.ALGORITHM
    secret_key = Config.SECRET_KEY
    expiry_time = Config.ACCESS_TOKEN_EXPIRE_DAYS

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + (
            expires_delta or timedelta(days=self.expiry_time)
        )

        to_encode.update({"jti": str(uuid.uuid4())})
        to_encode.update({"exp": expire})

        return jwt.encode(to_encode, key=self.secret_key, algorithm=self.algorithm)

    @staticmethod
    def get_token_data(token: str = Depends(oauth_scheme)) -> dict:
        try:
            payload = jwt.decode(
                token, key=Config.SECRET_KEY, algorithms=[Config.ALGORITHM]
            )
            return payload
        except jwt.InvalidTokenError:
            raise AuthService.credentials_exception  # Explicit class reference

    @staticmethod
    async def get_logged_user(
        session: AsyncSession = Depends(get_async_session),
        token_data: dict = Depends(get_token_data),
    ):
        email = token_data.get("email")
        role = token_data.get("role")

        if not email or not role:
            raise AuthService.credentials_exception

        statement = select(Customers).where(Customers.email == email)
        if role == "Vendor":
            statement = select(Vendors).where(Vendors.email == email)

        response = await session.exec(statement)
        user = response.first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"message": "User not found"},
            )

        return user

    async def role_checker(
        self, allowed_role: List[str], token_data=Depends(get_token_data)
    ):
        role = token_data.get("role")
        if not role:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Access token"
            )

        if role not in allowed_role:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"{role} Role is not allowed to access this resource",
            )

        return None

    def send_verification_email(self):
        # TODO: Implement email verification logic
        pass


# # 🚀 Key Takeaways
# # ✅ oauth_scheme is used indirectly to extract the token before calling get_token_data.
# # ✅ Even though get_token_data does not have Depends(oauth_scheme), FastAPI injects the extracted token.
# # ✅ This is part of FastAPI's dependency injection system, allowing clean separation of concerns.
# # ✅ If oauth_scheme is removed, FastAPI won’t know how to get the token, and requests will fail.
