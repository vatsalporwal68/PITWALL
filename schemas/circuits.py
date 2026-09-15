from pydantic import BaseModel


class CircuitCreate(BaseModel):
    name: str
    country: str


class CircuitResponse(BaseModel):
    id: int
    name: str
    country: str