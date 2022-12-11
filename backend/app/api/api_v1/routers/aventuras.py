import typing as t

from fastapi import APIRouter, Request, Depends, Response, HTTPException

from api.deps import get_db
from core.auth import get_current_active_superuser
from crud.crud_aventuras import (
    list_aventuras,
    create_new_aventuras,
    retreive_by_circuit,
    retreive_aventuras,
    delete_aventuras_by_id,
    update_aventuras_by_id,
)
from schemas import AventurasCreate, ShowAventuras

aventuras_router = r = APIRouter()


@r.get(
    "/aventuras",
    response_model=t.List[ShowAventuras],
    response_model_exclude_none=True,
)
async def aventuras_list(
    response: Response,
    db=Depends(get_db),
   # current_user=Depends(get_current_active_superuser),
):
    """
    Get all aventuras
    """
    aventuras = list_aventuras(db)
    # This is necessary for react-admin to work
    response.headers["Content-Range"] = f"0-10/{len(aventuras)}"
    return aventuras

@r.get(
    "/aventuras/by_circuit",
    response_model=t.List[ShowAventuras],
    response_model_exclude_none=True,
)
async def aventuras_list(
    response: Response,
    id_circuit: int,
    db=Depends(get_db),
   # current_user=Depends(get_current_active_superuser),
):
    """
    Get all aventuras
    """
    aventuras = retreive_by_circuit(id_circuit=id_circuit, db=db)
    # This is necessary for react-admin to work
    response.headers["Content-Range"] = f"0-10/{len(aventuras)}"
    return aventuras


@r.get(
    "/aventuras/{aventura_id}",
    response_model=ShowAventuras,
    response_model_exclude_none=True,
)
async def aventura_details(
    request: Request,
    aventura_id: int,
    db=Depends(get_db),
   # current_user=Depends(get_current_active_superuser),
):
    """
    Get any user details
    """
    aventura = retreive_aventuras(db=db, id=aventura_id)
    return aventura
    # return encoders.jsonable_encoder(
    #     user, skip_defaults=True, exclude_none=True,
    # )


@r.post("/aventuras", response_model=t.List[ShowAventuras], response_model_exclude_none=True)
async def _create(
    request: Request,
    aventura: AventurasCreate,
    id_circuit: int,
    db=Depends(get_db),
   # current_user=Depends(get_current_active_superuser),
):
    """
    Create a new user
    """
    create_new_aventuras(db=db, aventuras=aventura, id_circuit=id_circuit)
    return list_aventuras(db)


@r.put(
    "/aventuras", response_model=t.List[ShowAventuras], response_model_exclude_none=True
)
async def aventura_edit(
    request: Request,
    aventura_id: int,
    aventura: AventurasCreate,
    db=Depends(get_db),
   # current_user=Depends(get_current_active_superuser),
):
    """
    Update existing user
    """
    aventura_ = retreive_aventuras(db=db, id=aventura_id)
    if not aventura_:
        raise HTTPException(status_code=401, detail="aventura not found")
    update_aventuras_by_id(db=db,id=aventura_.id, aventuras=aventura)
    return list_aventuras(db)

@r.delete(
    "/aventuras", response_model=t.List[ShowAventuras], response_model_exclude_none=True
)
async def aventura_delete(
    request: Request,
    aventura_id: int,
    db=Depends(get_db),
   # current_user=Depends(get_current_active_superuser),
):
    """
    Delete existing user
    """
    aventura_ = retreive_aventuras(db=db, id=aventura_id)
    if not aventura_:
        raise HTTPException(status_code=401, detail="aventura not found")
    delete_aventuras_by_id(db=db, id=aventura_id)
    return list_aventuras(db)