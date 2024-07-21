from app.models.backtest import BacktestModel
from pydantic import ValidationError
from fastapi import HTTPException
from app.data.utils import stock_data


def process_backtest(backtest: BacktestModel):
    try:
        backtest.model_validate(backtest)
    except ValidationError as e:
        raise HTTPException(status_code=404, detail=e.errors())

    stock_data(backtest.ticker_data)
    return backtest
