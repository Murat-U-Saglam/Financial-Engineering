from fastapi import FastAPI
from app.endpoints.router import router as data_router
from app.endpoints.schema_endpoint import router as schema_router

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


app.include_router(router=data_router, prefix="/data", tags=["data"])

app.include_router(router=schema_router, prefix="/schema", tags=["schema"])
