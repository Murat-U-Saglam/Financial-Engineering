import yfinance as yf
import datetime as dt
import pandas as pd
from data.database import get_session


def get_stock_data(
    ticker: str, start_date: dt.datetime, end_data: dt.datetime = dt.datetime.now()
) -> pd.DataFrame:
    """All stock data is retrieved from Yahoo Finance API  with a 1 hr interval"""
    stock_data = yf.Ticker(ticker)
    history = stock_data.history(period="1h", start=start_date, end=end_data)
    return history
