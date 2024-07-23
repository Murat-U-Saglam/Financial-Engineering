from typing import Optional
from app.ORM.ticker import Tickers, StockData
from app.models.db_models import TickersModel
from app.data.database import get_session
from app.data.inbound_data import get_stock_data_from_api
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict
import datetime as dt


def stock_data(ticker_data: TickersModel):
    """
    stock_data is a function that is used to get stock data from the Yahoo Finance API and store it in the database.
    :param ticker_data: TickersModel
    :return: None
    """
    try:
        with get_session() as session:
            ticker = Tickers(
                ticker=ticker_data.ticker,
                date_from=ticker_data.date_from,
                date_to=ticker_data.date_to,
            )
            session.add(ticker)
            session.commit()
            data = get_stock_data_from_api(ticker_data)
            create_stock_data_from_dataframe(ticker=ticker_data.ticker, df=data)
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")


def create_ticker(ticker_model: TickersModel) -> None:
    """
    Create a new Ticker entry in the database.
    """
    with get_session() as session:
        ticker = Tickers(
            ticker=ticker_model.ticker,
            date_from=ticker_model.date_from,
            date_to=ticker_model.date_to,
        )
        session.add(ticker)
        session.commit()


def create_ticker_and_stock(ticker_model: TickersModel) -> None:
    """
    Create a new Ticker entry in the database.
    Checks if the ticker already exists to avoid duplicate primary key entries.
    """
    in_db = read_ticker(ticker_symbol=ticker_model.ticker)
    if in_db is None:
        data = get_stock_data_from_api(ticker_model)
        create_stock_data_from_dataframe(ticker=ticker_model.ticker, df=data)
        create_ticker(ticker_model)
    elif check_ticker_ranges(ticker_model=ticker_model, in_db=in_db):
        update_stock_data(ticker_data_model=ticker_model, in_db=in_db)


def check_ticker_ranges(ticker_model: TickersModel, in_db: Tickers) -> bool:
    """
    Check if the date ranges of the ticker_model are outside the ranges of the in_db ticker.
    If so, update the in_db ticker to reflect the new ranges.

    :param ticker_model: TickersModel instance with the new date ranges.
    :param in_db: Tickers instance with the current date ranges in the database.
    :return: True if the in_db ticker was updated, False otherwise.
    """
    update_needed = False

    # Check if the start date of ticker_model is before the start date of in_db
    if ticker_model.date_from < in_db.date_from:
        update_needed = True

    # Check if the end date of ticker_model is after the end date of in_db
    if ticker_model.date_to > in_db.date_to:
        update_needed = True

    return update_needed


def read_ticker(ticker_symbol: str) -> Optional[Tickers]:
    """
    Read a Ticker entry from the database by ticker symbol.
    Returns the Ticker object if found, else None.
    """
    with get_session() as session:
        ticker = session.query(Tickers).filter_by(ticker=ticker_symbol).first()
        return ticker
    ## TODO do checks for ranges of date and update accordingly


def update_ticker(ticker_model: TickersModel) -> None:
    """
    Update an existing Ticker entry in the database.
    """
    with get_session() as session:
        ticker = session.query(Tickers).filter_by(ticker=ticker_model.ticker).first()

        if ticker:
            if ticker_model.date_from is not None:
                ticker.date_from = ticker_model.date_from
            if ticker_model.date_to is not None:
                ticker.date_to = ticker_model.date_to
            session.commit()
        else:
            create_ticker(ticker_model)


def delete_ticker(ticker_symbol: str) -> None:
    """
    Delete a Ticker entry from the database by ticker symbol.
    """
    with get_session() as session:
        ticker = session.query(Tickers).filter_by(ticker=ticker_symbol).first()
        if ticker:
            session.delete(ticker)
            session.commit()
        else:
            raise ValueError(f"No ticker found with the symbol {ticker_symbol}.")


def create_stock_data_from_dataframe(ticker: str, df: pd.DataFrame):
    try:
        with get_session() as session:
            for index, row in df.iterrows():
                ticker = StockData(
                    date=index,
                    ticker=ticker,
                    open_price=row["Open"],
                    high_price=row["High"],
                    low_price=row["Low"],
                    close_price=row["Close"],
                    volume=row["Volume"],
                    dividends=row["Dividends"],
                    stock_splits=row["Stock Splits"],
                )
                session.add(ticker)
            session.commit()
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")


def get_stock_data_by_ticker(ticker_model: TickersModel) -> pd.DataFrame:
    with get_session() as session:
        stock_data = (
            session.query(StockData)
            .filter_by(ticker=ticker_model.ticker)
            .where(StockData.date >= ticker_model.date_from)
            .where(StockData.date <= ticker_model.date_to)
        )
        return stock_data


def update_stock_data(
    ticker_data_model: TickersModel, in_db: Tickers
) -> Dict[str, Dict[str, dt.date | None]]:
    """
    update_ticker_data Changes the meta data in the database if the new data is outside the old data range. Should call update_stock_data if the data range is changed.
    :rtype: Dict[str , Dict[str, dt.date | None]] {from: {old: dt.date, new: dt.date}, to: {old: dt.date, new: dt.date}}
    """
    changes: Dict[str, Dict[str, dt.date | None]] = {}
    with get_session() as session:
        if in_db.date_from < ticker_data_model.date_from:
            changes["from"]["old"], changes["from"]["new"] = (
                in_db.date_from,
                ticker_data_model.date_from,
            )
            data = get_stock_data_from_api(
                ticker_data_to_get=TickersModel(
                    ticker=ticker_data_model.ticker,
                    date_from=ticker_data_model.date_from,
                    date_to=in_db.date_from,
                )
            )
            create_stock_data_from_dataframe(ticker=ticker_data_model.ticker, df=data)
            in_db.date_from = ticker_data_model.date_from
            session.add(in_db)
            session.commit()
        elif ticker_data_model.date_to > in_db.date_to:
            changes["new"]["old"], changes["new"]["to"] = (
                in_db.date_to,
                ticker_data_model.date_to,
            )
            data = get_stock_data_from_api(
                ticker_data_to_get=TickersModel(
                    ticker=ticker_data_model.ticker,
                    date_from=in_db.date_from,
                    date_to=ticker_data_model.date_to,
                )
            )
            create_stock_data_from_dataframe(ticker=ticker_data_model.ticker, df=data)
            in_db.date_to = ticker_data_model.date_to
            session.add(in_db)
            session.commit()
        return changes


def delete_stock(ticker_id: int):
    try:
        with get_session() as session:
            ticker = session.query(Tickers).filter(Tickers.id == ticker_id).first()
            if ticker:
                session.delete(ticker)
                session.commit()
            else:
                print("Ticker not found")
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
