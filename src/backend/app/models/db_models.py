from pydantic import BaseModel, Field
import datetime as dt


class TickersModel(BaseModel):
    ticker: str = Field(default=..., max_length=5)
    date_from: dt.date
    date_to: dt.date = Field(default=dt.datetime.now().date())

    class Config:
        orm_mode = True


class StockDataModel(BaseModel):
    id: int
    ticker: str = Field(default=..., max_length=5)
    date: dt.date
    open_price: int
    close_price: int
    volume: int

    class Config:
        orm_mode = True
