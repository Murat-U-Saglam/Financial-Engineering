from pydantic import BaseModel, Field
import datetime as dt


class TickersModel(BaseModel):
    ticker: str = Field(default=..., max_length=5)
    date_from: dt.date
    date_to: dt.date = Field(default=dt.datetime.now().date())

    class Config:
        orm_mode = True
