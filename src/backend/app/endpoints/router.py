from fastapi import APIRouter


router = APIRouter()


@router.get("/backtest", status_code=200)
def get_backtest():
    """Ticker data, Risk profile, Strategies (greedy, random, etc), TA(indiciators)"""
    return {"message": "backtest"}
