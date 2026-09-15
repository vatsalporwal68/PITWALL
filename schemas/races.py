from pydantic import BaseModel


class RaceCreate(BaseModel):
    name: str
    circuit_id: int
    laps: int


class RaceResponse(BaseModel):
    id: int
    name: str
    circuit_id: int
    laps: int