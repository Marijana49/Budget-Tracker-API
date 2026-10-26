from fastapi import FastAPI
from contextlib import asynccontextmanager
from budget_tracker_api.database import create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

app = FastAPI(title="Budget Tracker API", lifespan=lifespan)

@app.get("/")
def proba():
    return {"message": "Moj projekat"}  