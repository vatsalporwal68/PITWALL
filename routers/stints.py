from fastapi import APIRouter, Depends, HTTPException

from database import get_db
from models import Stint as StintModel
from schemas.stints import (
    StintCreate,
    StintResponse,
    StintAnalysisResponse
)
from services.stint_service import analyze_stint as analyze_stint_service

router = APIRouter()


@router.get("/stints", response_model=list[StintResponse])
def get_stints(db=Depends(get_db)):

    stints = db.query(StintModel).all()

    return stints


@router.get("/stints/{stint_id}", response_model=StintResponse)
def get_stint(stint_id: int, db=Depends(get_db)):

    stint = (
        db.query(StintModel)
        .filter(StintModel.id == stint_id)
        .first()
    )

    if stint is None:
        raise HTTPException(
            status_code=404,
            detail="Stint not found"
        )

    return stint


@router.post(
    "/stints",
    response_model=StintResponse,
    status_code=201
)
def create_stint(stint: StintCreate, db=Depends(get_db)):

    new_stint = StintModel(
        race_entry_id=stint.race_entry_id,
        tyre_compound_id=stint.tyre_compound_id,
        start_lap=stint.start_lap,
        end_lap=stint.end_lap,
        tyre_age_start=stint.tyre_age_start
    )

    db.add(new_stint)
    db.commit()
    db.refresh(new_stint)

    return new_stint


@router.put("/stints/{stint_id}", response_model=StintResponse)
def update_stint(
    stint_id: int,
    updated_stint: StintCreate,
    db=Depends(get_db)
):

    stint = (
        db.query(StintModel)
        .filter(StintModel.id == stint_id)
        .first()
    )

    if stint is None:
        raise HTTPException(
            status_code=404,
            detail="Stint not found"
        )

    stint.race_entry_id = updated_stint.race_entry_id
    stint.tyre_compound_id = updated_stint.tyre_compound_id
    stint.start_lap = updated_stint.start_lap
    stint.end_lap = updated_stint.end_lap
    stint.tyre_age_start = updated_stint.tyre_age_start

    db.commit()
    db.refresh(stint)

    return stint


@router.delete("/stints/{stint_id}")
def delete_stint(stint_id: int, db=Depends(get_db)):

    stint = (
        db.query(StintModel)
        .filter(StintModel.id == stint_id)
        .first()
    )

    if stint is None:
        raise HTTPException(
            status_code=404,
            detail="Stint not found"
        )

    db.delete(stint)
    db.commit()

    return {
        "message": "Stint deleted successfully"
    }


@router.get(
    "/stints/{stint_id}/analysis",
    response_model=StintAnalysisResponse
)
def analyze_stint(stint_id: int, db=Depends(get_db)):

    result = analyze_stint_service(stint_id, db)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Stint not found"
        )

    return result

@router.get("/stints/{stint_id}/details")
def get_stint_details(
    stint_id: int,
    db=Depends(get_db)
):
    stint = (
        db.query(StintModel)
        .filter(StintModel.id == stint_id)
        .first()
    )

    if stint is None:
        raise HTTPException(
            status_code=404,
            detail="Stint not found"
        )

    return {
        "stint_id": stint.id,
        "driver": stint.race_entry.driver.name,
        "tyre": stint.tyre_compound.name,
        "start_lap": stint.start_lap,
        "end_lap": stint.end_lap
    }    