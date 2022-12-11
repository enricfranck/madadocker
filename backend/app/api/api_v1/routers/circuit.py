import typing as t

from fastapi import APIRouter, Request, Depends, Response, HTTPException

from api.deps import get_db
from core.auth import get_current_active_superuser
from crud.crud_circuit import (
    list_circuit,
    create_new_circuit,
    retreive_circuit,
    delete_circuit_by_id,
    update_circuit_by_id,
)
from schemas import CircuitCreate, ShowCircuit

circuit_router = r = APIRouter()


@r.get(
    "/circuits",
    response_model=t.List[ShowCircuit],
    response_model_exclude_none=True,
)
async def circuit_list(
    response: Response,
    db=Depends(get_db),
   # current_user=Depends(get_current_active_superuser),
):
    """
    Get all circuit
    """
    circuit = list_circuit(db)
    # This is necessary for react-admin to work
    response.headers["Content-Range"] = f"0-10/{len(circuit)}"
    return circuit


@r.get(
    "/circuits/{circuit_id}",
    response_model=ShowCircuit,
    response_model_exclude_none=True,
)
async def circuit_details(
    request: Request,
    circuit_id: int,
    db=Depends(get_db),
   # current_user=Depends(get_current_active_superuser),
):
    """
    Get any user details
    """
    circuit = retreive_circuit(db=db, id=circuit_id)
    return circuit
    # return encoders.jsonable_encoder(
    #     user, skip_defaults=True, exclude_none=True,
    # )


@r.post("/circuits", response_model=t.List[ShowCircuit], response_model_exclude_none=True)
async def _create(
    request: Request,
    circuit: CircuitCreate,
    db=Depends(get_db),
   # current_user=Depends(get_current_active_superuser),
):
    """
    Create a new user
    """
    create_new_circuit(db=db, circuit=circuit)
    return list_circuit(db)


@r.put(
    "/circuits", response_model=t.List[ShowCircuit], response_model_exclude_none=True
)
async def circuit_edit(
    request: Request,
    circuit_id: int,
    circuit: CircuitCreate,
    db=Depends(get_db),
   # current_user=Depends(get_current_active_superuser),
):
    """
    Update existing user
    """
    circuit_ = retreive_circuit(db=db, id=circuit_id)
    if not circuit_:
        raise HTTPException(status_code=401, detail="circuit not found")
    update_circuit_by_id(db=db,id=circuit_.id, circuit=circuit)
    return list_circuit(db)


@r.delete(
    "/circuits", response_model=t.List[ShowCircuit], response_model_exclude_none=True
)
async def circuit_delete(
    request: Request,
    circuit_id: int,
    db=Depends(get_db),
   # current_user=Depends(get_current_active_superuser),
):
    """
    Delete existing user
    """
    circuit_ = retreive_circuit(db=db, id=circuit_id)
    if not circuit_:
        raise HTTPException(status_code=401, detail="circuit not found")
    delete_circuit_by_id(db=db, id=circuit_id)
    return list_circuit(db)