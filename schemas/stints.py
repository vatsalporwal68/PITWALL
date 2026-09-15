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