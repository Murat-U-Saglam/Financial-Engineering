from fastapi import APIRouter
from app.models.backtest import BacktestModel
from app.endpoints.behaviour import process_backtest

router = APIRouter()


@router.get("/backtest", status_code=200)
def get_backtest(backtest: BacktestModel):
    return {"message": "backtest"}
