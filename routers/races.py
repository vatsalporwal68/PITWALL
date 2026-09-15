from fastapi import APIRouter, Depends, HTTPException

from database import get_db
from models import Race as RaceModel
from schemas.races import RaceCreate, RaceResponse


router = APIRouter()


@router.get("/races", response_model=list[RaceResponse])
def get_races(db=Depends(get_db)):
    races = db.query(RaceModel).all()
    return races


@router.get("/races/{race_id}", response_model=RaceResponse)
def get_race(race_id: int, db=Depends(get_db)):
    race = (
        db.query(RaceModel)
        .filter(RaceModel.id == race_id)
        .first()
    )

    if race is None:
        raise HTTPException(
            status_code=404,
            detail="Race not found"
        )

    return race


@router.post(
    "/races",
    response_model=RaceResponse,
    status_code=201
)
def create_race(
    race: RaceCreate,
    db=Depends(get_db)
):
    new_race = RaceModel(
        name=race.name,
        circuit_id=race.circuit_id,
        laps=race.laps
    )

    db.add(new_race)
    db.commit()
    db.refresh(new_race)

    return new_race


@router.put(
    "/races/{race_id}",
    response_model=RaceResponse
)
def update_race(
    race_id: int,
    updated_race: RaceCreate,
    db=Depends(get_db)
):
    race = (
        db.query(RaceModel)
        .filter(RaceModel.id == race_id)
        .first()
    )

    if race is None:
        raise HTTPException(
            status_code=404,
            detail="Race not found"
        )

    race.name = updated_race.name
    race.circuit_id = updated_race.circuit_id
    race.laps = updated_race.laps

    db.commit()
    db.refresh(race)

    return race


@router.delete("/races/{race_id}")
def delete_race(
    race_id: int,
    db=Depends(get_db)
):
    race = (
        db.query(RaceModel)
        .filter(RaceModel.id == race_id)
        .first()
    )

    if race is None:
        raise HTTPException(
            status_code=404,
            detail="Race not found"
        )

    db.delete(race)
    db.commit()

    return {
        "message": "Race deleted successfully"
    }