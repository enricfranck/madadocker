from datetime import date
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# shared properties
class CarBase(BaseModel):
    name: Optional[str] = None
    url_car: Optional[str] = None


# this will be used to validate data while creating a Job
class CarCreate(CarBase):
    name: str
    url_car: str


# this will be used to format the response to not to have id,owner_id etc
class ShowCar(CarBase):
    id: int
    name: str
    url_car: str

    class Config:  # to convert non dict obj to json
        orm_mode = True
