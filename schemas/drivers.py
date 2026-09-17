from pydantic import BaseModel, ConfigDict


class DriverCreate(BaseModel):
    name: str
    number: int
    team_id: int


class TeamInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    nationality: str


class DriverResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    number: int
    team_id: int
    team: TeamInfo