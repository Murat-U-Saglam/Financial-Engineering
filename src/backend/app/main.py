from fastapi import FastAPI
import os

print(os.getcwd())
from app.endpoints.router import router as data_router

app = FastAPI(
    title="Tools for finance",
    version="0.1",
    description="Tools to develop my ETL process for finance data",
    docs_url="/",
    redoc_url="/redoc",
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/ping")
async def ping():
    return {"ping": "a"}


app.include_router(data_router, prefix="/data", tags=["data"])
