from pydantic import BaseModel, EmailStr
from datetime import datetime
import uuid
from typing import Optional

class UserCreateModel(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    phone_no: str


class UserGetModel(UserCreateModel):
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime


class UserLoginModel(BaseModel):
    email: EmailStr
    password: str
    phone_no: Optional [str]

class token(BaseModel):
    access_token: str
    token_type: str

class tokendata(BaseModel):
    id : Optional [str] = None
