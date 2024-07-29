from pydantic import field_validator, ConfigDict
import datetime as dt
from dateutil.relativedelta import relativedelta
from fastapi import HTTPException
from sqlmodel import SQLModel, Field


class StockData(SQLModel, table=True):
    __tablename__ = "stock_data"
    id: int = Field(default=None, primary_key=True)
    ticker: str = Field(default=None, max_length=5)
    date: dt.date = Field(default=None)
    open: float = Field(default=None)
    high: float = Field(default=None)
    low: float = Field(default=None)
    close: float = Field(default=None)
    adj_close: float = Field(default=None)
    volume: int = Field(default=None)


class Tickers(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    ticker: str = Field(default="APPL", max_length=5)
    date_to: dt.date = Field(default=dt.datetime.now().date())
    date_from: dt.date = Field(
        default=(dt.datetime.now() + relativedelta(years=-1)).date()
    )

    @field_validator("date_from")
    def validate_date_range(cls, value, values):
        date_to = values.get("date_to")
        if date_to and value > date_to:
            raise HTTPException(
                status_code=400,
                detail="date_from must be less than or equal to date_to",
            )
        return value

    @field_validator("date_to")
    def validate_date_to(cls, value, values):
        if value >= dt.datetime.now().date() + relativedelta(days=1):
            raise HTTPException(
                status_code=400, detail="date_to must be less than or equal to today"
            )
        return value

    class Config:
        arbitrary_types_allowed = True
