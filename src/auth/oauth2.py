from typing import Optional
import uuid
import jwt
from datetime import timedelta, datetime, timezone
from src.config import Config


class AuthService:
    algorithm = Config.ALGORITHM
    secret_key = Config.SECRET_KEY
    expiry_time = Config.ACCESS_TOKEN_EXPIRE_DAYS

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

    def verify_access_token(self, token, credentials_exception) -> dict:
        try:
            payload = jwt.decode(
                token, key=self.secret_key, algorithms=[self.algorithm]
            )

            if payload.get("email") is None:
                raise credentials_exception

            return payload

        except jwt.InvalidTokenError:
            raise credentials_exception

    def send_verification_email(self):
        # TODO: Implement email verification logic
        pass
