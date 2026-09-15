from pydantic import BaseModel


class LapCreate(BaseModel):
    race_entry_id: int
    lap_number: int
    lap_time: float


class LapResponse(BaseModel):
    id: int
    race_entry_id: int
    lap_number: int
    lap_time: float

class LapAnalysisResponse(BaseModel):
    lap_id: int
    lap_time: float
    sector_total: float
    difference: float
    sector_count: int    