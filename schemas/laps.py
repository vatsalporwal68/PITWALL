from pydantic import BaseModel, ConfigDict, Field


class LapCreate(BaseModel):
    race_entry_id: int
    lap_number: int = Field(gt=0)
    lap_time: float = Field(gt=0)

class RaceEntryInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    driver_id: int
    grid_position: int
    status: str


class LapResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    race_entry_id: int
    lap_number: int
    lap_time: float
    race_entry: RaceEntryInfo


class LapAnalysisResponse(BaseModel):
    lap_id: int
    lap_time: float
    sector_total: float
    difference: float
    sector_count: int   