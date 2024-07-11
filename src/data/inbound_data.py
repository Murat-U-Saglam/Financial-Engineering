import yfinance as yf
import datetime as dt
import pandas as pd
from data.database import get_session


def get_stock_data(ticker: str, date: dt.datetime) -> pd.DataFrame:
    stock_data = yf.Ticker(ticker)
    history = stock_data.history(period="1d", start=date, end=dt.datetime.now())
    return history
