from fastapi import APIRouter, Request, Depends, Response, HTTPException, UploadFile, File
import typing as t
import os
from fastapi.responses import FileResponse

from api.deps import get_db
from crud.crud_car import (
    list_cars,
    create_new_car,
    retreive_car,
    delete_car_by_id,
    update_car_by_id,
)
from schemas import CarCreate, ShowCar
from core.auth import get_current_active_user, get_current_active_superuser

cars_router = r = APIRouter()


@r.get(
    "/cars",
    response_model=t.List[ShowCar],
    response_model_exclude_none=True,
)
async def cars_list(
    response: Response,
    db=Depends(get_db),
   # current_user=Depends(get_current_active_superuser),
):
    """
    Get all cars
    """
    cars = list_cars(db)
    # This is necessary for react-admin to work
    response.headers["Content-Range"] = f"0-9/{len(cars)}"
    return cars


@r.get(
    "/cars/{car_id}",
    response_model=ShowCar,
    response_model_exclude_none=True,
)
async def car_details(
    request: Request,
    car_id: int,
    db=Depends(get_db),
   # current_user=Depends(get_current_active_superuser),
):
    """
    Get any user details
    """
    car = retreive_car(db=db, id=car_id)
    return car
    # return encoders.jsonable_encoder(
    #     user, skip_defaults=True, exclude_none=True,
    # )


@r.post("/cars", response_model=t.List[ShowCar], response_model_exclude_none=True)
async def _create(
    request: Request,
    car: CarCreate,
    db=Depends(get_db),
   # current_user=Depends(get_current_active_superuser),
):
    """
    Create a new user
    """
    create_new_car(db=db, car=car)
    return list_cars(db)


@r.put(
    "/cars", response_model=ShowCar, response_model_exclude_none=True
)
async def car_edit(
    request: Request,
    car_id: int,
    car: CarCreate,
    db=Depends(get_db),
   # current_user=Depends(get_current_active_superuser),
):
    """
    Update existing user
    """
    car_ = retreive_car(db=db, id=car_id)
    if not car_:
        raise HTTPException(status_code=401, detail="car not found")
    return update_car_by_id(db=db, car=car)


@r.delete(
    "/cars", response_model=t.List[ShowCar], response_model_exclude_none=True
)
async def car_delete(
    request: Request,
    car_id: int,
    db=Depends(get_db),
   # current_user=Depends(get_current_active_superuser),
):
    """
    Delete existing user
    """
    car_ = retreive_car(db=db, id=car_id)
    if not car_:
        raise HTTPException(status_code=401, detail="car not found")
    url = car_.url_car
    delete_car_by_id(db=db, id=car_id)
    path = os.getcwd() + "/files/" + url
    os.remove(path)
    return list_cars(db)


@r.get("/image/")
def get_file(image_name: str):
    path = os.getcwd() + "/files/" + image_name
    if os.path.exists(path):
        return FileResponse(path=path)
    return "Image not found"


@r.post("/upload/")
async def create_upload_file(*,
                             uploaded_file: UploadFile = File(...),
                             image_name: str,
                            # current_user= Depends(get_current_active_superuser)
                             ):
    name = list(os.path.splitext(uploaded_file.filename))[1]
    allowed_files = {".jpg", ".jpeg", ".png", ".webp"}

    if name.lower() not in allowed_files:
        raise HTTPException(status_code=402, detail="invalid image")
    file_location = f"files/{image_name}{name}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())
    return {"filename": f'{image_name}{name}'}
