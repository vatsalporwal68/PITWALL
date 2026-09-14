from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from database import SessionLocal
from models import Race as RaceModel

app = FastAPI()


class Race(BaseModel):
    id: int
    name: str
    circuit: str
    laps: int

@app.get("/")
def home():
    return {"message": "Welcome to PITWALL"}

@app.get("/races", response_model=list[Race])
def get_races():
    db = SessionLocal()

    try:
        races = db.query(RaceModel).all()
        return races
    finally:
        db.close()    


@app.get("/races/{race_id}", response_model=Race)
def get_race(race_id: int):
    db = SessionLocal()

    try:
        race = db.query(RaceModel).filter(RaceModel.id == race_id).first()

        if race is None:
            raise HTTPException(status_code=404, detail="Race not found")

        return Race(
            id=race.id,
            name=race.name,
            circuit=race.circuit,
            laps=race.laps
        )

    finally:
        db.close()

@app.post("/races", response_model=Race, status_code=201)
def create_race(race: Race):
    db = SessionLocal()

    try:
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

    finally:
        db.close()

@app.put("/races/{race_id}", response_model=Race)
def update_race(race_id: int, updated_race: Race):
    db = SessionLocal()

    try:
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

    finally:
        db.close()

@app.delete("/races/{race_id}")
def delete_race(race_id: int):
    db = SessionLocal()

    try:
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

    finally:
        db.close()       