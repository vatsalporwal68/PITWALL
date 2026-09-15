from pydantic import BaseModel


class TyreCompoundCreate(BaseModel):
    name: str
    tyre_type: str


class TyreCompoundResponse(BaseModel):
    id: int
    name: str
    tyre_type: str