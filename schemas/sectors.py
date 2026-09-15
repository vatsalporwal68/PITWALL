from pydantic import BaseModel


class SectorCreate(BaseModel):
    lap_id: int
    sector_number: int
    sector_time: float


class SectorResponse(BaseModel):
    id: int
    lap_id: int
    sector_number: int
    sector_time: float