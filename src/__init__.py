from fastapi import Depends, FastAPI
from sqlmodel.ext.asyncio.session import AsyncSession
from src.config import Config
from src.db.main import get_async_session, init_db
from src.users.routes import users_router
from src.vehicles.routes import vehicles_router
from contextlib import asynccontextmanager


@asynccontextmanager
async def life_span(app: FastAPI):
    print("Server starts")
    await init_db()
    yield
    print("Server ends")


VERSION = "V1"
app = FastAPI(
    title="WheelXchange",
    version=VERSION,
    description="A Rest API for Vehicle Rental system or Market Place",
    lifespan=life_span,
)


@app.get("/")
async def root(session: AsyncSession = Depends(get_async_session)):
    return {
        "title": "WheelXchange",
        "moto": "List. Rent. Ride. Repeat!",
        "subtitle": "Where Owners Earn & Renters Roll!",
        "DB_URI": Config.DB_URI,
    }


app.include_router(users_router, prefix=f"/api/{VERSION}/users", tags=["Users"])
app.include_router(
    vehicles_router, prefix=f"/api/{VERSION}/vehicles", tags=["Vehicles"]
)
