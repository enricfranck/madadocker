from models import Aventuras
from schemas import AventurasCreate
from sqlalchemy.orm import Session


def create_new_aventuras(aventuras: AventurasCreate, db: Session):
    aventuras_object = Aventuras(**aventuras.dict())
    db.add(aventuras_object)
    db.commit()
    db.refresh(aventuras_object)
    return aventuras_object


def retreive_aventuras(id: int, db: Session):
    item = db.query(Aventuras).filter(Aventuras.id == id).first()
    return item


def list_aventuras(db: Session):
    aventuras = db.query(Aventuras).all()
    return aventuras


def update_aventuras_by_id(id: int, aventuras: AventurasCreate, db: Session):
    existing_aventuras = db.query(Aventuras).filter(Aventuras.id == id)
    if not existing_aventuras.first():
        return 0
    aventuras.__dict__.update(
    )  # update dictionary with new key value of owner_id
    existing_aventuras.update(aventuras.__dict__)
    db.commit()
    return 1


def delete_aventuras_by_id(id: int, db: Session):
    existing_aventuras = db.query(Aventuras).filter(Aventuras.id == id)
    if not existing_aventuras.first():
        return 0
    existing_aventuras.delete(synchronize_session=False)
    db.commit()
    return 1


def search_aventuras(query: str, db: Session):
    aventuras = db.query(Aventuras).filter(Aventuras.title.contains(query))
    return aventuras
