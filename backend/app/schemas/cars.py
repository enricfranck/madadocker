from datetime import date
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# shared properties
class CarBase(BaseModel):
    name: Optional[str] = None
    url_image: Optional[str] = None
    description: Optional[str] = None


# this will be used to validate data while creating a Job
class CarCreate(CarBase):
    name: Optional[str] 
    url_image: Optional[str]
    description: Optional[str] 

# this will be used to format the response to not to have id,owner_id etc
class ShowCar(CarBase):
    id: int
    name: str
    description: Optional[str] 
    url_image: str

    class Config:  # to convert non dict obj to json
        orm_mode = True
