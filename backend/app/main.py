from fastapi import FastAPI, Depends
from starlette.requests import Request
import uvicorn
from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from starlette.middleware.cors import CORSMiddleware
from api.api_v1.routers.users import users_router
from api.api_v1.routers.aventuras import aventuras_router
from api.api_v1.routers.cars import cars_router
from api.api_v1.routers.auth import auth_router
from api.deps import get_db
from crud.crud_aventuras import list_aventuras
from core import config
from fastapi.staticfiles import StaticFiles
from db.init_db import init_db
from db.session import SessionLocal
from core.auth import get_current_active_user
from core.celery_app import celery_app

from webapps.base import api_router as web_app_router

templates = Jinja2Templates(directory="app/templates")
app = FastAPI(
    title=config.PROJECT_NAME, docs_url="/api/docs", openapi_url="/api"
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response


@app.get("/api/v1")
async def home(request: Request, db: Session = Depends(get_db), msg: str = None):
    adventures = list_aventuras(db=db)
    return templates.TemplateResponse(
        "index.html", {"request": request, "adventures": adventures, "msg": msg}
    )
@app.get("/api/v1/about_us")
async def about_us(request: Request):
    return templates.TemplateResponse(
        "about-us.html", {"request": request}
    )

@app.get("/api/v1/circuit")
async def circuit(request: Request, db: Session = Depends(get_db), msg: str = None):
    circuits = list_aventuras(db=db)
    return templates.TemplateResponse(
        "circuit.html", {"request": request, "circuits": circuits, "msg": msg}
    )

@app.get("/api/v1/customer_protection")
async def customer_protection(request: Request):
    return templates.TemplateResponse(
        "customer-protection.html", {"request": request}
    )

@app.get("/api/v1/our_offer")
async def our_offer(request: Request):
    return templates.TemplateResponse(
        "our-offer.html", {"request": request}
    )

@app.get("/api/v1/contact")
async def contact(request: Request):
    return templates.TemplateResponse(
        "contact.html", {"request": request}
    )


@app.get("/api/v1/api/v1/task")
async def example_task():
    celery_app.send_task("app.tasks.example_task", args=["Hello World"])

    return {"message": "success"}


# Routers
app.include_router(
    users_router,
    prefix="/api/v1",
    tags=["users"],
    dependencies=[Depends(get_current_active_user)],
)

app.include_router(
    cars_router,
    prefix="/api/v1",
    tags=["cars"],
    #dependencies=[Depends(get_current_active_user)],
)

app.include_router(
    aventuras_router,
    prefix="/api/v1",
    tags=["aventuras"],
    #dependencies=[Depends(get_current_active_user)],
)
app.include_router(auth_router, prefix="/api", tags=["auth"])
app.include_router(web_app_router)

if __name__ == "__main__":
    init_db()
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)
