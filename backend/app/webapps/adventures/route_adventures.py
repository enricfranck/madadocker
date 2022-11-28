
from crud.crud_aventuras import (
    list_aventuras
)
from api.deps import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session


templates = Jinja2Templates(directory="app/templates")
router = APIRouter(include_in_schema=False)


@router.get("/")
async def home(request: Request, db: Session = Depends(get_db), msg: str = None):
    adventures = list_aventuras(db=db)
    return templates.TemplateResponse(
        "index.html", {"request": request, "adventures": adventures, "msg": msg}
    )

@router.get("/about_us")
async def about_us(request: Request):
    return templates.TemplateResponse(
        "about-us.html", {"request": request}
    )

@router.get("/circuit")
async def circuit(request: Request, db: Session = Depends(get_db), msg: str = None):
    circuits = list_aventuras(db=db)
    return templates.TemplateResponse(
        "circuit.html", {"request": request, "circuits": circuits, "msg": msg}
    )

@router.get("/customer_protection")
async def customer_protection(request: Request):
    return templates.TemplateResponse(
        "customer-protection.html", {"request": request}
    )

@router.get("/our_offer")
async def our_offer(request: Request):
    return templates.TemplateResponse(
        "our-offer.html", {"request": request}
    )

@router.get("/contact")
async def contact(request: Request):
    return templates.TemplateResponse(
        "contact.html", {"request": request}
    )
