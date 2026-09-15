from pydantic import BaseModel


class StintCreate(BaseModel):
    race_entry_id: int
    tyre_compound_id: int
    start_lap: int
    end_lap: int | None = None
    tyre_age_start: int = 0


class StintResponse(BaseModel):
    id: int
    race_entry_id: int
    tyre_compound_id: int
    start_lap: int
    end_lap: int | None
    tyre_age_start: int
    

class StintAnalysisResponse(BaseModel):
    stint_id: int
    lap_count: int
    average_lap_time: float | None
    best_lap_time: float | None
    worst_lap_time: float | None