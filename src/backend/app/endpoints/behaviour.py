from app.models.backtest import BacktestModel
from pydantic import ValidationError
from fastapi import HTTPException
from pandas import DataFrame
from app.data.utils import create_ticker_and_stock, get_stock_data_by_ticker


def process_backtest(backtest: BacktestModel) -> DataFrame:
    try:
        backtest.model_validate(backtest)
    except ValidationError as e:
        raise HTTPException(status_code=404, detail=e.errors())

    create_ticker_and_stock(backtest.ticker_data)
    df = get_stock_data_by_ticker(backtest.ticker_data)

    return df
