from fastapi import APIRouter

from src.vehicles.service import CarService

vehicles_router = APIRouter()
car_service = CarService()


@vehicles_router.get("/cars")
def get_all_cars():
    pass


@vehicles_router.get("/cars/{uid}")
def get_car():
    pass


@vehicles_router.post("/cars")
def create_car():
    pass


@vehicles_router.patch("/cars/{uid}")
def edit_car():
    pass


@vehicles_router.delete("/cars/{uid}")
def delete_car():
    pass
