from fastapi import FastAPI
from src.users.routes import users_router
from src.vehicles.routes import vehicles_router

VERSION = "V1"
app = FastAPI(
    title="WheelXchange",
    version=VERSION,
    description="A Rest API for Vehicle Rental system or Market Place",
)


@app.get("/")
async def root():
    return {
        "title": "WheelXchange",
        "moto": "List. Rent. Ride. Repeat!",
        "subtitle": "Where Owners Earn & Renters Roll!",
    }


app.include_router(users_router, prefix=f"/api/{VERSION}/users", tags=["Users"])
app.include_router(
    vehicles_router, prefix=f"/api/{VERSION}/vehicles", tags=["Vehicles"]
)
