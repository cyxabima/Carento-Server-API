from typing import List
from fastapi import Depends, HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import BaseUser, Customers, Vendors
from src.db.main import get_async_session
from src.auth.oauth2 import AuthService
from fastapi.security import OAuth2PasswordBearer

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")
auth_service = AuthService()
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_token_data(token=Depends(oauth_scheme)):
    token_data = auth_service.verify_access_token(token, credentials_exception)
    return token_data


async def get_logged_user(
    session: AsyncSession = Depends(get_async_session),
    token=Depends(oauth_scheme),
) -> BaseUser:

    token_data = auth_service.verify_access_token(token, credentials_exception)
    email = token_data.get("email")
    role = token_data.get("role")

    if not email or not role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

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


# why use a higher order function because dependency takes only reference of function
def role_checker(allowed_role: List[str]):
    def _role_dependency(token=Depends(oauth_scheme), _=Depends(get_logged_user)):
        token_data = auth_service.verify_access_token(token, credentials_exception)
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

        return True

    return _role_dependency


# Dependencies
customer_dependency = Depends(role_checker(["Admin", "Customer"]))
vendor_dependency = Depends(role_checker(["Admin", "Vendor"]))
review_dependency = Depends(role_checker(["Admin", "Customer"]))
