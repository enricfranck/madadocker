from models import Circuit
from schemas import CircuitCreate
from sqlalchemy.orm import Session


def create_new_circuit(circuit: CircuitCreate, db: Session):
    circuit_object = Circuit(**circuit.dict())
    db.add(circuit_object)
    db.commit()
    db.refresh(circuit_object)
    return circuit_object


def retreive_circuit(id: int, db: Session):
    item = db.query(Circuit).filter(Circuit.id == id).first()
    return item


def list_circuit(db: Session):
    circuit = db.query(Circuit).all()
    return circuit


def update_circuit_by_id(id: int, circuit: CircuitCreate, db: Session):
    existing_circuit = db.query(Circuit).filter(Circuit.id == id)
    if not existing_circuit.first():
        return 0
    circuit.__dict__.update(
    )  # update dictionary with new key value of owner_id
    existing_circuit.update(circuit.__dict__)
    db.commit()
    return 1


def delete_circuit_by_id(id: int, db: Session):
    existing_circuit = db.query(Circuit).filter(Circuit.id == id)
    if not existing_circuit.first():
        return 0
    existing_circuit.delete(synchronize_session=False)
    db.commit()
    return 1


def search_circuit(query: str, db: Session):
    circuit = db.query(Circuit).filter(Circuit.title.contains(query))
    return circuit
