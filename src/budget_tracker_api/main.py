from fastapi import FastAPI
from contextlib import asynccontextmanager
from budget_tracker_api.database import create_tables
from budget_tracker_api.exception_handlers import register_exception_handlers
from budget_tracker_api.routes import categories, transactions

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

app = FastAPI(title="Budget Tracker API", lifespan=lifespan)

register_exception_handlers(app)

app.include_router(categories.router)
app.include_router(transactions.router)

@app.get("/")
def proba():
    return {"message": "Moj projekat"}  