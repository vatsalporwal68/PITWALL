from fastapi import FastAPI

from routers.races import router as races_router
from routers.circuits import router as circuits_router
from routers.teams import router as teams_router


app = FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome to PITWALL"}


app.include_router(races_router)
app.include_router(circuits_router)
app.include_router(teams_router)     