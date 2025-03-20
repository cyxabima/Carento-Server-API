from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_async_session
from src.vehicles.schemas import CarCreateModel, CarGetModel, CarUpdateModel
from src.vehicles.service import CarService

vehicles_router = APIRouter()
car_service = CarService()


@vehicles_router.get("/cars", response_model=List[CarGetModel])
async def get_all_cars(db: AsyncSession = Depends(get_async_session)):
    cars = await car_service.get_all_cars(db)
    return cars


@vehicles_router.get("/cars/{car_uid}", response_model=CarGetModel)
async def get_car(
    car_uid: str,
    db: AsyncSession = Depends(get_async_session),
):
    car = await car_service.get_car(car_uid, db)
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "car with this uid is not found"},
        )
    return car


@vehicles_router.post(
    "/cars",
    status_code=status.HTTP_201_CREATED,
    response_model=CarGetModel,
)
async def create_car(
    car_data: CarCreateModel, db: AsyncSession = Depends(get_async_session)
):
    car = await car_service.create_car(car_data, db)

    if not car:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "error while creating car"},
        )
    return car


@vehicles_router.patch("/cars/{car_uid}", response_model=CarGetModel)
async def edit_car(
    car_uid: str,
    car_update_data: CarUpdateModel,
    db: AsyncSession = Depends(get_async_session),
):
    car = await car_service.edit_car(car_uid, car_update_data, db)
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "car with this uid is not found"},
        )
    return car


@vehicles_router.delete("/cars/{car_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_car(car_uid: str, db: AsyncSession = Depends(get_async_session)):
    car = await car_service.delete_car(car_uid, db)

    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "car with this uid is not found"},
        )

    return
