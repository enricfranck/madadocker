from db.base_class import Base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String


class Aventuras(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    direction = Column(String, nullable=False)
    description = Column(String, nullable=False)
