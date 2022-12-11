from db.base_class import Base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String


class Car(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    url_image = Column(String, nullable=False)
    description = Column(String, nullable=True)
