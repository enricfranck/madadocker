from datetime import date
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# shared properties
class AventurasBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    direction: Optional[str] = None


# this will be used to validate data while creating a Job
class AventurasCreate(AventurasBase):
    title: str
    direction: str
    description: str


# this will be used to format the response to not to have id,owner_id etc
class ShowAventuras(AventurasBase):
    id: int
    title: str
    direction: str
    description: str

    class Config:  # to convert non dict obj to json
        orm_mode = True
