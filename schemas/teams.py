from pydantic import BaseModel


class TeamCreate(BaseModel):
    name: str
    nationality: str


class TeamResponse(BaseModel):
    id: int
    name: str
    nationality: str