from pydantic import BaseModel, Field
from datetime import date


class TickersModel(BaseModel):
    ticker: str = Field(default=..., max_length=5)
    date_from: date
    date_to: date

    class Config:
        orm_mode = True


class StockDataModel(BaseModel):
    id: int
    ticker: str = Field(default=..., max_length=5)
    date: date
    open_price: int
    close_price: int
    volume: int

    class Config:
        orm_mode = True
