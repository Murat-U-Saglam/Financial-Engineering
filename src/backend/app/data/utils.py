from data.inbound_data import get_stock_data
import datetime as dt
from data.ORM.input_models import create_stock_data_class, StockDataFields
from data.database import get_session
import pandas as pd


def in_db(ticker: str) -> bool | StockDataFields:
    ticker_stock_data = create_stock_data_class(ticker)
    if ticker_stock_data is None:
        return False
    return ticker_stock_data


def write_stock_data_to_db(ticker_stock_data: StockDataFields) -> None:
    with get_session() as session:
        session.add(ticker_stock_data)
        session.commit()


def get_stock_data_from_db(ticker_stock_data: StockDataFields) -> pd.DataFrame:
    with get_session() as session:
        session.query(ticker_stock_data)
        session.commit()
        return pd.DataFrame(ticker_stock_data)


def options_data(ticker: str, date: dt.datetime) -> pd.DataFrame:
    data = in_db(ticker)
    if data:
        data = get_stock_data_from_db(ticker_stock_data=data)
        return data
    data = get_stock_data(ticker, date)
    write_stock_data_to_db(data)
    return data
