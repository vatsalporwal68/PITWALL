from fastapi import APIRouter, Depends, HTTPException

from database import get_db
from models import RaceEntry as RaceEntryModel
from schemas.race_entries import RaceEntryCreate, RaceEntryResponse


router = APIRouter()


@router.get(
    "/race-entries",
    response_model=list[RaceEntryResponse]
)
def get_race_entries(db=Depends(get_db)):
    entries = db.query(RaceEntryModel).all()
    return entries


@router.get(
    "/race-entries/{entry_id}",
    response_model=RaceEntryResponse
)
def get_race_entry(entry_id: int, db=Depends(get_db)):
    entry = (
        db.query(RaceEntryModel)
        .filter(RaceEntryModel.id == entry_id)
        .first()
    )

    if entry is None:
        raise HTTPException(
            status_code=404,
            detail="Race entry not found"
        )

    return entry


@router.post(
    "/race-entries",
    response_model=RaceEntryResponse,
    status_code=201
)
def create_race_entry(
    entry: RaceEntryCreate,
    db=Depends(get_db)
):
    new_entry = RaceEntryModel(
        race_id=entry.race_id,
        driver_id=entry.driver_id,
        grid_position=entry.grid_position,
        finishing_position=entry.finishing_position,
        points=entry.points,
        status=entry.status
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return new_entry


@router.put(
    "/race-entries/{entry_id}",
    response_model=RaceEntryResponse
)
def update_race_entry(
    entry_id: int,
    updated_entry: RaceEntryCreate,
    db=Depends(get_db)
):
    entry = (
        db.query(RaceEntryModel)
        .filter(RaceEntryModel.id == entry_id)
        .first()
    )

    if entry is None:
        raise HTTPException(
            status_code=404,
            detail="Race entry not found"
        )

    entry.race_id = updated_entry.race_id
    entry.driver_id = updated_entry.driver_id
    entry.grid_position = updated_entry.grid_position
    entry.finishing_position = updated_entry.finishing_position
    entry.points = updated_entry.points
    entry.status = updated_entry.status

    db.commit()
    db.refresh(entry)

    return entry


@router.delete("/race-entries/{entry_id}")
def delete_race_entry(
    entry_id: int,
    db=Depends(get_db)
):
    entry = (
        db.query(RaceEntryModel)
        .filter(RaceEntryModel.id == entry_id)
        .first()
    )

    if entry is None:
        raise HTTPException(
            status_code=404,
            detail="Race entry not found"
        )

    db.delete(entry)
    db.commit()

    return {
        "message": "Race entry deleted successfully"
    }