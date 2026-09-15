from pydantic import BaseModel


class RaceEntryCreate(BaseModel):
    race_id: int
    driver_id: int
    grid_position: int
    finishing_position: int | None = None
    points: float = 0
    status: str


class RaceEntryResponse(BaseModel):
    id: int
    race_id: int
    driver_id: int
    grid_position: int
    finishing_position: int | None
    points: float
    status: str