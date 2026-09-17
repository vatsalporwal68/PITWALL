from pydantic import BaseModel, ConfigDict


class SectorCreate(BaseModel):
    lap_id: int
    sector_number: int
    sector_time: float


class LapInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    race_entry_id: int
    lap_number: int
    lap_time: float


class SectorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lap_id: int
    sector_number: int
    sector_time: float
    lap: LapInfo