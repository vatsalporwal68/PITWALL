from fastapi import APIRouter, Depends, HTTPException

from database import get_db
from models import TyreCompound as TyreCompoundModel
from schemas.tyres import (
    TyreCompoundCreate,
    TyreCompoundResponse
)


router = APIRouter()


@router.get(
    "/tyres",
    response_model=list[TyreCompoundResponse]
)
def get_tyres(db=Depends(get_db)):
    tyres = db.query(TyreCompoundModel).all()
    return tyres


@router.get(
    "/tyres/{tyre_id}",
    response_model=TyreCompoundResponse
)
def get_tyre(tyre_id: int, db=Depends(get_db)):
    tyre = (
        db.query(TyreCompoundModel)
        .filter(TyreCompoundModel.id == tyre_id)
        .first()
    )

    if tyre is None:
        raise HTTPException(
            status_code=404,
            detail="Tyre compound not found"
        )

    return tyre


@router.post(
    "/tyres",
    response_model=TyreCompoundResponse,
    status_code=201
)
def create_tyre(
    tyre: TyreCompoundCreate,
    db=Depends(get_db)
):
    new_tyre = TyreCompoundModel(
        name=tyre.name,
        tyre_type=tyre.tyre_type
    )

    db.add(new_tyre)
    db.commit()
    db.refresh(new_tyre)

    return new_tyre


@router.put(
    "/tyres/{tyre_id}",
    response_model=TyreCompoundResponse
)
def update_tyre(
    tyre_id: int,
    updated_tyre: TyreCompoundCreate,
    db=Depends(get_db)
):
    tyre = (
        db.query(TyreCompoundModel)
        .filter(TyreCompoundModel.id == tyre_id)
        .first()
    )

    if tyre is None:
        raise HTTPException(
            status_code=404,
            detail="Tyre compound not found"
        )

    tyre.name = updated_tyre.name
    tyre.tyre_type = updated_tyre.tyre_type

    db.commit()
    db.refresh(tyre)

    return tyre


@router.delete("/tyres/{tyre_id}")
def delete_tyre(tyre_id: int, db=Depends(get_db)):
    tyre = (
        db.query(TyreCompoundModel)
        .filter(TyreCompoundModel.id == tyre_id)
        .first()
    )

    if tyre is None:
        raise HTTPException(
            status_code=404,
            detail="Tyre compound not found"
        )

    db.delete(tyre)
    db.commit()

    return {
        "message": "Tyre compound deleted successfully"
    }