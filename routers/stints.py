from fastapi import APIRouter, Depends, HTTPException

from database import get_db
from models import Stint as StintModel, Lap as LapModel
from schemas.stints import (
    StintCreate,
    StintResponse,
    StintAnalysisResponse
)

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

    query = (
        db.query(LapModel)
        .filter(
            LapModel.race_entry_id == stint.race_entry_id,
            LapModel.lap_number >= stint.start_lap
        )
    )

    if stint.end_lap is not None:
        query = query.filter(
            LapModel.lap_number <= stint.end_lap
        )

    laps = query.order_by(
        LapModel.lap_number
    ).all()

    lap_times = [
        lap.lap_time
        for lap in laps
    ]

    if not lap_times:
        return {
            "stint_id": stint.id,
            "lap_count": 0,
            "average_lap_time": None,
            "best_lap_time": None,
            "worst_lap_time": None
        }

    return {
        "stint_id": stint.id,
        "lap_count": len(lap_times),
        "average_lap_time": round(
            sum(lap_times) / len(lap_times),
            3
        ),
        "best_lap_time": min(lap_times),
        "worst_lap_time": max(lap_times)
    }

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