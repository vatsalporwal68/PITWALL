from fastapi import FastAPI
from routers.races import router as races_router

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to PITWALL"}

app.include_router(races_router)      