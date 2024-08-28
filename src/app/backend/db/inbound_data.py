import yfinance as yf
import pandas as pd
from backend.models.backtest import Tickers


async def get_stock_data_from_api(ticker_data_to_get: Tickers) -> pd.DataFrame:
    stock_data = yf.Ticker(ticker=ticker_data_to_get.ticker)
    history = stock_data.history(
        period="1d", start=ticker_data_to_get.date_from, end=ticker_data_to_get.date_to
    )
    if history.empty:
        raise ValueError("No data found for the given ticker")
    return history
