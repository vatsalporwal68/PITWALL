from pydantic import BaseModel


class RaceCreate(BaseModel):
    name: str
    circuit: str
    laps: int


class RaceResponse(BaseModel):
    id: int
    name: str
    circuit: str
    laps: int