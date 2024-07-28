from typing import Optional
from app.models.models import Tickers, StockData
from app.data.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from app.data.inbound_data import get_stock_data_from_api
import pandas as pd
from typing import Dict
from sqlmodel import Session, select
import datetime as dt
from fastapi import Depends, HTTPException, status
from . import logger


async def stock_data(ticker_data: Tickers, session: AsyncSession = get_session) -> None:
    """
    stock_data is a function that is used to get stock data from the Yahoo Finance API and store it in the database.
    :param ticker_data: Tickers
    :return: None
    """
    ticker = Tickers(
        ticker=ticker_data.ticker,
        date_from=ticker_data.date_from,
        date_to=ticker_data.date_to,
    )
    session.add(ticker)
    session.commit()
    data = get_stock_data_from_api(ticker_data)
    create_stock_data_from_dataframe(ticker=ticker_data.ticker, df=data)


async def create_ticker(
    ticker_model: Tickers, session: AsyncSession = get_session
) -> None:
    """
    Create a new Ticker entry in the database.
    """

    bomba = Tickers(
        ticker=ticker_model.ticker,
        date_from=ticker_model.date_from,
        date_to=ticker_model.date_to,
    )
    session.add(bomba)
    await session.commit()


async def create_ticker_and_stock(
    ticker_model: Tickers, session: AsyncSession = get_session
) -> None:
    """
    Create a new Ticker entry in the database.
    Checks if the ticker already exists to avoid duplicate primary key entries.
    """
    in_db = await read_ticker(ticker_symbol=ticker_model.ticker, session=session)
    if in_db is None:
        data = await get_stock_data_from_api(ticker_data_to_get=ticker_model)
        await create_stock_data_from_dataframe(
            ticker=ticker_model.ticker, df=data, session=session
        )
        await create_ticker(ticker_model=ticker_model, session=session)
    elif await check_ticker_ranges(
        ticker_model=ticker_model, in_db=in_db, session=session
    ):
        await update_stock_data(tickers_model=ticker_model, in_db=in_db)


async def check_ticker_ranges(
    ticker_model: Tickers, in_db: Tickers, session: AsyncSession = get_session
) -> bool:
    """
    Check if the date ranges of the ticker_model are outside the ranges of the in_db ticker.
    If so, update the in_db ticker to reflect the new ranges.

    :param ticker_model: Tickers instance with the new date ranges.
    :param in_db: Tickers instance with the current date ranges in the database.
    :return: True if the in_db ticker was updated, False otherwise.
    """
    update_needed = False
    if ticker_model.date_from is None or ticker_model.date_to is None:
        update_needed = True
        return update_needed

    # Check if the start date of ticker_model is before the start date of in_db
    if ticker_model.date_from < in_db.date_from:
        update_needed = True
        return update_needed

    # Check if the end date of ticker_model is after the end date of in_db
    if ticker_model.date_to > in_db.date_to:
        update_needed = True
        return update_needed

    return False


async def read_ticker(
    ticker_symbol: str, session: AsyncSession = get_session
) -> Optional[Tickers]:
    """
    Read a Ticker entry from the database by ticker symbol.
    Returns the Ticker object if found, else None."""
    statement = select(Tickers).where(Tickers.ticker == ticker_symbol)
    result = await session.execute(statement)
    ticker = result.scalars().first()
    if ticker is None:
        logger.error(f"No ticker found with the symbol {ticker_symbol}.")
    return ticker


async def update_ticker(
    ticker_model: Tickers, session: AsyncSession = get_session
) -> None:
    """
    Update an existing Ticker entry in the database.
    """
    ticker = await session.query(Tickers).filter_by(ticker=ticker_model.ticker).first()
    if not ticker:
        raise ValueError(f"No ticker found with the symbol {ticker_model.ticker}.")
    ticker.date_from = ticker_model.date_from
    ticker.date_to = ticker_model.date_to
    session.commit()


async def delete_ticker(
    ticker_symbol: str, session: AsyncSession = get_session
) -> None:
    """
    Delete a Ticker entry from the database by ticker symbol.
    """
    async with session as session:
        ticker = session.query(Tickers).filter_by(ticker=ticker_symbol).first()
        if ticker:
            session.delete(ticker)
            session.commit()
        else:
            raise ValueError(f"No ticker found with the symbol {ticker_symbol}.")


def df_to_db(session: Session, df: pd.DataFrame) -> bool:
    conn = session.connection()
    df.to_sql(name="stock_data", con=conn, if_exists="replace", index=True)
    session.commit()


async def create_stock_data_from_dataframe(
    ticker: str, df: pd.DataFrame, session: AsyncSession = get_session
) -> None:
    df["Ticker"] = ticker
    df.reset_index(inplace=True)
    await session.run_sync(df_to_db, df)  ## Needs to be done non Async


async def get_stock_data_by_ticker(
    ticker_model: Tickers, session: AsyncSession = get_session
) -> pd.DataFrame:
    ticker = ticker_model.ticker
    date_from = ticker_model.date_from
    date_to = ticker_model.date_to
    ## FIX THIS
    statement = (
        select(StockData)
        .join(Tickers)
        .where(
            Tickers.ticker == ticker,
            StockData.date >= date_from,
            StockData.date <= date_to,
        )
    )
    result = await session.execute(statement)
    session_data = result.scalars().all()
    return pd.DataFrame([data.__dict__ for data in session_data])


async def check_if_update_is_required(
    tickers_model: Tickers, in_db: Tickers
) -> Dict[str, bool] | None:
    changes: Dict[str, bool] = {"date_from": False, "date_to": False}
    if tickers_model.date_from < in_db.date_from:
        changes["date_from"] = True
    if tickers_model.date_to > in_db.date_to:
        changes["date_to"] = True
    if in_db.date_from is None:
        changes["date_from"] = True
    if in_db.date_to is None:
        changes["date_to"] = True
    if not any(changes.values()):
        return None
    return changes


async def update_stock_data(
    tickers_model: Tickers, in_db: Tickers, session: AsyncSession = get_session
) -> None:
    changes = check_if_update_is_required(tickers_model, in_db)
    if not changes:
        return None
    if changes.get("date_from"):
        df = get_stock_data_from_api(
            ticker_data_to_get=Tickers(
                ticker=tickers_model.ticker,
                date_from=tickers_model.date_from,
                date_to=in_db.date_from,
            )
        )
        create_stock_data_from_dataframe(ticker=tickers_model.ticker, df=df)
    if changes.get("date_to"):
        df = get_stock_data_from_api(
            ticker_data_to_get=Tickers(
                ticker=tickers_model.ticker,
                date_from=in_db.date_to,
                date_to=tickers_model.date_to,
            )
        )
        create_stock_data_from_dataframe(ticker=tickers_model.ticker, df=df)
    update_ticker(tickers_model)


async def delete_stock(
    ticker_id: int, session: AsyncSession = get_session
) -> Dict[str, str]:
    ticker = session.get(Tickers, ticker_id)
    if not ticker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticker not found {ticker_id}",
        )
    session.delete(ticker)
    session.commit()
    return {"message": "Ticker deleted successfully"}
