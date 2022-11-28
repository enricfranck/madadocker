from api.deps import get_db
from crud.crud_car import (
    list_cars,
    retreive_car,
)
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session


templates = Jinja2Templates(directory="app/templates")
router = APIRouter(include_in_schema=False)


@router.get("/cars")
async def cars(request: Request, db: Session = Depends(get_db), msg: str = None):
    cars = list_cars(db=db)
    return templates.TemplateResponse(
        "car.html", {"request": request, "cars": cars, "msg": msg}
    )