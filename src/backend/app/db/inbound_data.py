import yfinance as yf
import pandas as pd
from app.models.SQLModel import Tickers
from fastapi import HTTPException


async def get_stock_data_from_api(ticker_data_to_get: Tickers) -> pd.DataFrame:
    stock_data = yf.Ticker(ticker=ticker_data_to_get.ticker)
    history = stock_data.history(period= "1d",  start=ticker_data_to_get.date_from, end=ticker_data_to_get.date_to
    )
    if history.empty:
        raise HTTPException(
            status_code=400,
            detail=f"Error retrieving stock data: {ticker_data_to_get.ticker}",
        )
    return history
