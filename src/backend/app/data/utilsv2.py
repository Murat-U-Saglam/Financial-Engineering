from typing import Optional
from ORM.ticker import Tickers, StockData
from models.db_models import TickersModel
from data.database import get_session

from sqlalchemy.exc import IntegrityError


def create_ticker(ticker_model: TickersModel) -> None:
    """
    Create a new Ticker entry in the database.
    Checks if the ticker already exists to avoid duplicate primary key entries.
    """
    with get_session() as session:
        # Check if the ticker already exists
        existing_ticker = (
            session.query(Tickers).filter_by(ticker=ticker_model.ticker).first()
        )
        if existing_ticker:
            # Handle the duplicate entry as per your application's requirements
            # For example, raise an exception or return a message
            raise ValueError(
                f"A ticker with the symbol {ticker_model.ticker} already exists."
            )
        else:
            # If no existing ticker, proceed to create a new one
            ticker = Tickers(
                ticker=ticker_model.ticker,
                date_from=ticker_model.date_from,
                date_to=ticker_model.date_to,
            )
            session.add(ticker)
            try:
                session.commit()
            except IntegrityError:
                session.rollback()
                raise ValueError(
                    "Failed to create ticker due to a database integrity error."
                )


def read_ticker(ticker_symbol: str) -> Optional[Tickers]:
    """
    Read a Ticker entry from the database by ticker symbol.
    Returns the Ticker object if found, else None.
    """
    with get_session() as session:
        ticker = session.query(Tickers).filter_by(ticker=ticker_symbol).first()
        return ticker


def update_ticker(ticker_model: TickersModel) -> None:
    """
    Update an existing Ticker entry in the database.
    """
    with get_session() as session:
        ticker = session.query(Tickers).filter_by(ticker=ticker_model.ticker).first()
        if ticker:
            ticker.date_from = ticker_model.date_from
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


import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from src.backend.app.ORM.ticker import Tickers, get_session


def create_tickers_from_dataframe(ticker : str, df: pd.DataFrame):
    try:
        with get_session() as session:
            for index, row in df.iterrows():
                ticker = StockData(
                    date=index,
                    ticker = ticker,
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

    
def get_stock_data_by_ticker(ticker_symbol: str):
    with get_session() as session:
        stock_data = session.query(StockData).filter_by(ticker=ticker_symbol).all()
        return stock_data

def update_stock_range(ticker_id, update_data: dict):
    """
    update_stock_range This gets metadata for a ticker and updates it in the database. with the new ranges of stock data.
    #TODO Change the function to update the stock data in the database
    """
    try:
        with get_session() as session:
            ticker = session.query(Tickers).filter(Tickers.id == ticker_id).first()
            if ticker:
                for key, value in update_data.items():
                    setattr(ticker, key, value)
                session.commit()
            else:
                print("Ticker not found")
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")


def delete_ticker(ticker_id: int):
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
