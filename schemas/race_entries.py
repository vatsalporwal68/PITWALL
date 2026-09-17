from pydantic import BaseModel, ConfigDict


class RaceEntryCreate(BaseModel):
    race_id: int
    driver_id: int
    grid_position: int
    finishing_position: int | None = None
    points: float = 0
    status: str


class RaceInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    laps: int


class DriverInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    number: int


class RaceEntryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    race_id: int
    driver_id: int
    grid_position: int
    finishing_position: int | None
    points: float
    status: str
    race: RaceInfo
    driver: DriverInfo