from typing import List

from models import Car
from schemas import CarCreate
from sqlalchemy.orm import Session


def create_new_car(car: CarCreate, db: Session):
    car_object = Car(**car.dict())
    db.add(car_object)
    db.commit()
    db.refresh(car_object)
    return car_object


def retreive_car(id: int, db: Session)-> Car:
    item = db.query(Car).filter(Car.id == id).first()
    return item


def list_cars(db: Session)->List[Car]:
    cars = db.query(Car).all()
    return cars


def update_car_by_id(id: int, car: CarCreate, db: Session):
    existing_car = db.query(Car).filter(Car.id == id)
    if not existing_car.first():
        return 0
    car.__dict__.update(
    )  # update dictionary with new key value of owner_id
    existing_car.update(car.__dict__)
    db.commit()
    return 1


def delete_car_by_id(id: int, db: Session):
    existing_car = db.query(Car).filter(Car.id == id)
    if not existing_car.first():
        return 0
    existing_car.delete(synchronize_session=False)
    db.commit()
    return 1


def search_car(query: str, db: Session):
    cars = db.query(Car).filter(Car.title.contains(query))
    return cars
