from pydantic import BaseModel, Field
import datetime as dt
from dateutil.relativedelta import relativedelta


class TickersModel(BaseModel):
    ticker: str = Field(default="APPL", max_length=5)
    date_from: dt.date = Field(
        default=(dt.datetime.now() + relativedelta(years=-1)).date()
    )
    date_to: dt.date = Field(default=dt.datetime.now().date())

    class Config:
        orm_mode = True
