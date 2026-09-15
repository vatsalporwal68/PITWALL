from pydantic import BaseModel


class DriverCreate(BaseModel):
    name: str
    number: int
    team_id: int


class DriverResponse(BaseModel):
    id: int
    name: str
    number: int
    team_id: int