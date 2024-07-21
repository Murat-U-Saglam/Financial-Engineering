from pydantic import BaseModel, Field, validator
import datetime as dt
from dateutil.relativedelta import relativedelta
from fastapi import HTTPException


class TickersModel(BaseModel):
    ticker: str = Field(default="APPL", max_length=5)
    date_to: dt.date = Field(default=dt.datetime.now().date())
    date_from: dt.date = Field(
        default=(dt.datetime.now() + relativedelta(years=-1)).date()
    )

    @validator("date_from")
    def validate_date_range(cls, value, values):
        date_to = values.get("date_to")
        if date_to and value > date_to:
            raise HTTPException(
                status_code=400,
                detail="date_from must be less than or equal to date_to",
            )
        return value

    @validator("date_to")
    def validate_date_to(cls, value, values):
        if value >= dt.datetime.now().date() + relativedelta(days=1):
            raise HTTPException(
                status_code=400, detail="date_to must be less than or equal to today"
            )
        return value

    class Config:
        from_attributes = True
