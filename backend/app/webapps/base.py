from fastapi import APIRouter
from webapps.adventures import route_adventures
from webapps.cars import route_cars


api_router = APIRouter()
api_router.include_router(route_adventures.router, prefix="", tags=["adventure-webapp"])
api_router.include_router(route_cars.router, prefix="", tags=["cars-webapp"])
