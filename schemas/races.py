from pydantic import BaseModel, ConfigDict


class RaceCreate(BaseModel):
    name: str
    circuit_id: int
    laps: int


class CircuitInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    country: str


class RaceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    circuit_id: int
    laps: int
    circuit: CircuitInfo