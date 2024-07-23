from fastapi import APIRouter
from app.models.backtest import BacktestModel
from app.endpoints.behaviour import process_backtest
from fastapi.responses import JSONResponse
from . import logger
from pandas import DataFrame
from . import logger

router = APIRouter()


@router.post("/backtest", status_code=200)
def get_backtest(backtest: BacktestModel):
    logger.info(msg=f"Received backtest request for {backtest}")
    df = process_backtest(backtest)
    logger.error(df)
    return JSONResponse(content=df, status_code=200)
