from datetime import date
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# shared properties
class CircuitBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    url_image: Optional[str] = None


# this will be used to validate data while creating a Job
class CircuitCreate(CircuitBase):
    title: str
    url_image: str
    description: Optional[str] 


# this will be used to format the response to not to have id,owner_id etc
class ShowCircuit(CircuitBase):
    id: int
    title: str
    url_image: str
    description: Optional[str] 

    class Config:  # to convert non dict obj to json
        orm_mode = True
