from fastapi import APIRouter
from app.models.backtest import BacktestModel
from app.endpoints.behaviour import process_backtest
from fastapi.responses import JSONResponse
from . import logger

router = APIRouter()


@router.post("/backtest", status_code=200)
def get_backtest(backtest: BacktestModel):
    logger.error(f"Received backtest request for {backtest}")
    # validate backtest
    process_backtest(backtest)
    return JSONResponse(content="Backtest Successful Bomba", status_code=200)
