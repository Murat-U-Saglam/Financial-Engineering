from fastapi import APIRouter
from app.models.backtest import BacktestModel
from app.endpoints.behaviour import process_backtest
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/backtest", status_code=200)
def get_backtest(backtest: BacktestModel):
    return JSONResponse(content="Backtest Successful Bomba", status_code=200)
