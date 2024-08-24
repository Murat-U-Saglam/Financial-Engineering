from typing import Optional
from app.models.SQLModel import Tickers
from app.db.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.inbound_data import get_stock_data_from_api
import pandas as pd
from typing import Dict
from sqlmodel import Session, select
from fastapi import HTTPException, status, Depends
from . import logger


async def stock_data(ticker_data: Tickers, session: AsyncSession = Depends(dependency=get_session)) -> None:
    """
    stock_data is a function that is used to get stock data from the Yahoo Finance API and store it in the database.
    :param ticker_data: Tickers
    :return: None
    """
    await session.add(ticker_data)
    await session.commit()
    data = await get_stock_data_from_api(ticker_data_to_get=ticker_data)
    await create_stock_data_from_dataframe(
        ticker=ticker_data.ticker, df=data, session=session
    )


async def create_ticker_in_db(
    ticker_model: Tickers, session: AsyncSession = Depends(dependency=get_session)
) -> None:
    """Create a new Ticker entry in the database."""
    session.add(ticker_model)
    await session.commit()


async def create_ticker_and_stock(
    ticker_model: Tickers, session: AsyncSession = Depends(dependency=get_session)
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
        await create_ticker_in_db(ticker_model=ticker_model, session=session)

    elif await check_ticker_ranges(
        ticker_model=ticker_model, in_db=in_db, session=session
    ):
        await update_stock_data(
            tickers_model=ticker_model, in_db=in_db, session=session
        )


async def check_ticker_ranges(
    ticker_model: Tickers, in_db: Tickers, session: AsyncSession = Depends(dependency=get_session)
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
    ticker_symbol: str, session: AsyncSession = Depends(dependency=get_session)
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
    ticker_model: Tickers, session: AsyncSession = Depends(dependency=get_session)
) -> None:
    """
    Update an existing Ticker entry in the database.
    """
    # ticker = await session.execute(select(Tickers).filter_by(ticker=ticker_model.ticker).first()
    ticker = await read_ticker(ticker_symbol=ticker_model.ticker, session=session)
    if not ticker:
        raise ValueError(f"No ticker found with the symbol {ticker_model.ticker}.")
    ticker.date_from = ticker_model.date_from
    ticker.date_to = ticker_model.date_to


async def delete_ticker(
    ticker_symbol: str, session: AsyncSession = Depends(dependency=get_session)
) -> None:
    """
    Delete a Ticker entry from the database by ticker symbol.
    """
    ticker = await read_ticker(ticker_symbol=ticker_symbol, session=session)
    if ticker:
        await session.delete(ticker)
        await session.commit()
    else:
        raise ValueError(f"No ticker found with the symbol {ticker_symbol}.")


def df_to_db(session: Session, df: pd.DataFrame) -> None:
    conn = session.connection()
    df.to_sql(name="stock_data", con=conn, if_exists="replace", index=True)
    session.commit()


async def create_stock_data_from_dataframe(
    ticker: str, df: pd.DataFrame, session: AsyncSession = Depends(dependency=get_session)
) -> None:
    df["Ticker"] = ticker
    df.reset_index(inplace=True)
    await session.run_sync(df_to_db, df)  ## Needs to be done non Async


def get_stock_data_by_ticker(session: Session, ticker_model: Tickers) -> pd.DataFrame:
    conn = session.connection()
    df = pd.read_sql(
        f"SELECT * FROM stock_data WHERE Ticker = '{ticker_model.ticker}' AND Date >= '{ticker_model.date_from}' AND Date <= '{ticker_model.date_to}'",
        con=conn,
    )
    return df


async def update_stock_data(
    tickers_model: Tickers, in_db: Tickers, session: AsyncSession = Depends(dependency=get_session)
) -> None:
    if in_db.date_from is None or tickers_model.date_from < in_db.date_from:
        new_date_from = tickers_model.date_from
    else:
        new_date_from = in_db.date_from
    if in_db.date_to is None or tickers_model.date_to > in_db.date_to:
        new_date_to = tickers_model.date_to
    else:
        new_date_to = in_db.date_to
    tmp_ticker_model = Tickers(
        ticker=in_db.ticker, date_from=new_date_from, date_to=new_date_to
    )
    df = await get_stock_data_from_api(ticker_data_to_get=tmp_ticker_model)
    await create_stock_data_from_dataframe(ticker=in_db.ticker, df=df, session=session)
    await update_ticker(ticker_model=tmp_ticker_model, session=session)


async def delete_stock(
    ticker_id: int, session: AsyncSession = Depends(dependency=get_session)
) -> Dict[str, str]:
    ticker = session.get(Tickers, ticker_id)
    if not ticker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticker not found {ticker_id}",
        )
    await session.delete(ticker)
    await session.commit()
    return {"message": "Ticker deleted successfully"}
