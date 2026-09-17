from fastapi import APIRouter, Depends, HTTPException

from database import get_db
from models import Lap as LapModel, Sector as SectorModel
from schemas.laps import LapAnalysisResponse, LapCreate, LapResponse


router = APIRouter()


@router.get("/laps", response_model=list[LapResponse])
def get_laps(db=Depends(get_db)):
    laps = db.query(LapModel).all()
    return laps


@router.get("/laps/{lap_id}", response_model=LapResponse)
def get_lap(lap_id: int, db=Depends(get_db)):
    lap = (
        db.query(LapModel)
        .filter(LapModel.id == lap_id)
        .first()
    )

    if lap is None:
        raise HTTPException(
            status_code=404,
            detail="Lap not found"
        )

    return lap

@router.get(
    "/laps/{lap_id}/analysis",
    response_model=LapAnalysisResponse
)
def analyze_lap(lap_id: int, db=Depends(get_db)):
    lap = (
        db.query(LapModel)
        .filter(LapModel.id == lap_id)
        .first()
    )

    if lap is None:
        raise HTTPException(
            status_code=404,
            detail="Lap not found"
        )

    sectors = (
        db.query(SectorModel)
        .filter(SectorModel.lap_id == lap_id)
        .all()
    )

    sector_total = sum(sector.sector_time for sector in sectors)

    difference = round(lap.lap_time - sector_total, 3)

    return {
        "lap_id": lap.id,
        "lap_time": lap.lap_time,
        "sector_total": sector_total,
        "difference": difference,
        "sector_count": len(sectors)
    }    


@router.post(
    "/laps",
    response_model=LapResponse,
    status_code=201
)
def create_lap(lap: LapCreate, db=Depends(get_db)):
    new_lap = LapModel(
        race_entry_id=lap.race_entry_id,
        lap_number=lap.lap_number,
        lap_time=lap.lap_time
    )

    db.add(new_lap)
    db.commit()
    db.refresh(new_lap)

    return new_lap


@router.put(
    "/laps/{lap_id}",
    response_model=LapResponse
)
def update_lap(
    lap_id: int,
    updated_lap: LapCreate,
    db=Depends(get_db)
):
    lap = (
        db.query(LapModel)
        .filter(LapModel.id == lap_id)
        .first()
    )

    if lap is None:
        raise HTTPException(
            status_code=404,
            detail="Lap not found"
        )

    lap.race_entry_id = updated_lap.race_entry_id
    lap.lap_number = updated_lap.lap_number
    lap.lap_time = updated_lap.lap_time

    db.commit()
    db.refresh(lap)

    return lap


@router.delete("/laps/{lap_id}")
def delete_lap(lap_id: int, db=Depends(get_db)):
    lap = (
        db.query(LapModel)
        .filter(LapModel.id == lap_id)
        .first()
    )

    if lap is None:
        raise HTTPException(
            status_code=404,
            detail="Lap not found"
        )

    db.delete(lap)
    db.commit()

    return {
        "message": "Lap deleted successfully"
    }

@router.get("/laps/{lap_id}/details")
def get_lap_details(
    lap_id: int,
    db=Depends(get_db)
):
    lap = (
        db.query(LapModel)
        .filter(LapModel.id == lap_id)
        .first()
    )

    if lap is None:
        raise HTTPException(
            status_code=404,
            detail="Lap not found"
        )

    return {
        "lap_number": lap.lap_number,
        "lap_time": lap.lap_time,
        "race_entry_id": lap.race_entry.id,
        "driver": lap.race_entry.driver.name
    }    