from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from database import get_db
from models import Race as RaceModel


router = APIRouter()


class Race(BaseModel):
    id: int
    name: str
    circuit: str
    laps: int


@router.get("/races", response_model=list[Race])
def get_races(db=Depends(get_db)):
    races = db.query(RaceModel).all()
    return races


@router.get("/races/{race_id}", response_model=Race)
def get_race(race_id: int, db=Depends(get_db)):
    race = db.query(RaceModel).filter(RaceModel.id == race_id).first()

    if race is None:
        raise HTTPException(status_code=404, detail="Race not found")

    return Race(
        id=race.id,
        name=race.name,
        circuit=race.circuit,
        laps=race.laps
    )


@router.post("/races", response_model=Race, status_code=201)
def create_race(race: Race, db=Depends(get_db)):
    new_race = RaceModel(
        id=race.id,
        name=race.name,
        circuit=race.circuit,
        laps=race.laps
    )

    db.add(new_race)
    db.commit()

    return Race(
        id=new_race.id,
        name=new_race.name,
        circuit=new_race.circuit,
        laps=new_race.laps
    )


@router.put("/races/{race_id}", response_model=Race)
def update_race(race_id: int, updated_race: Race, db=Depends(get_db)):
    race = db.query(RaceModel).filter(RaceModel.id == race_id).first()

    if race is None:
        raise HTTPException(status_code=404, detail="Race not found")

    race.name = updated_race.name
    race.circuit = updated_race.circuit
    race.laps = updated_race.laps

    db.commit()

    return Race(
        id=race.id,
        name=race.name,
        circuit=race.circuit,
        laps=race.laps
    )


@router.delete("/races/{race_id}")
def delete_race(race_id: int, db=Depends(get_db)):
    race = db.query(RaceModel).filter(RaceModel.id == race_id).first()

    if race is None:
        raise HTTPException(status_code=404, detail="Race not found")

    db.delete(race)
    db.commit()

    return {
        "message": "Race deleted successfully",
        "race": {
            "id": race.id,
            "name": race.name,
            "circuit": race.circuit,
            "laps": race.laps
        }
    }