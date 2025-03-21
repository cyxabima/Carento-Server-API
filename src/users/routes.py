from fastapi import APIRouter
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_async_session
from src.users.schemas import UserCreateModel, UserGetModel
from src.users.service import *

users_router = APIRouter()
owner_service = OwnerService
renter_service = RenterService

# add all rotes which is necessary
# owner login,signup,logout
# renter login,signup,logout
# create user model as well

# @users_router.post('/ownerlogin')