from pydantic import PastDate
import datetime as dt

from dateutil.relativedelta import relativedelta
from fastapi import HTTPException
from sqlmodel import SQLModel, Field, Date
from typing import Optional


class StockData(SQLModel, table=True):
    __tablename__ = "stock_data"
    index: int | None = Field(default=None, primary_key=True)
    ticker: str = Field(default=None, max_length=10)
    date: dt.date = Field(default=None)
    open: float = Field(default=None)
    high: float = Field(default=None)
    low: float = Field(default=None)
    close: float = Field(default=None)
    volume: int = Field(default=None)


class Tickers(SQLModel, table=True):
    class Config:
        arbitrary_types_allowed = True
        validate_assignment = True

    id: Optional[int] = Field(default=None, primary_key=True)
    ticker: str = Field(
        default="AAPL",
        max_length=10,
    )
    date_to: PastDate = Field(
        default=(dt.datetime.now().date() - dt.timedelta(days=2)), sa_type=Date
    )
    date_from: PastDate = Field(
        default=(dt.datetime.now() + relativedelta(years=-1)).date(), sa_type=Date
    )
