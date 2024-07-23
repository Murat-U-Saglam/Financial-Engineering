from fastapi import FastAPI
from app.endpoints.router import router as data_router
from app.endpoints.schema_endpoint import router as schema_router
from app.data.database import create_tables
from contextlib import asynccontextmanager





@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        create_tables()
        yield
    finally:
        pass
app = FastAPI(
    title="Tools for finance",
    version="0.1",
    description="Tools to develop my ETL process for finance data",
    docs_url="/",
    redoc_url="/redoc",lifespan=lifespan
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/ping")
async def ping():
    return {"ping": "a"}


app.include_router(router=data_router, prefix="/data", tags=["data"])

app.include_router(router=schema_router, prefix="/schema", tags=["schema"])
