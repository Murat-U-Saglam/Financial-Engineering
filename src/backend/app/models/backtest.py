from pydantic import BaseModel, Field, field_validator, PastDate
from enum import Enum
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import datetime as dt
from fastapi import HTTPException
from dateutil.relativedelta import relativedelta


class RiskLevel(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RiskProfileModel(BaseModel):
    risk_level: RiskLevel = Field(default=RiskLevel.MEDIUM, description="Risk Level")


# https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/bollinger-bands#:~:text=Bollinger%20Bands%20are%20envelopes%20plotted,swings%20in%20the%20underlying%20price.
class TAIndicator(BaseModel):
    moving_average: int = Field(
        default=30, ge=1, le=60, description="Moving Average duration - Close"
    )
    rsi: int = Field(
        default=14,
        ge=1,
        le=50,
        description="Relative Strength Index - Moving Average length",
    )


class Tickers(BaseModel):
    ticker: str = Field(default="AAPL", max_length=5)
    date_to: PastDate = Field(default=dt.datetime.now().date())
    date_from: PastDate = Field(
        default=(dt.datetime.now() + relativedelta(years=-1)).date()
    )

    @field_validator("date_from")
    def validate_date_from(cls, value, values):
        if value >= values.data["date_to"]:
            raise HTTPException(
                status_code=400, detail="date_from must be smaller than date_to"
            )
        return value


class StrategyLevel(Enum):
    GREEDY = "greedy"
    RANDOM = "random"


class Strategy(BaseModel):
    strategy: StrategyLevel = Field(
        default=StrategyLevel.GREEDY, description="Strategy Level"
    )


class BacktestModel(BaseModel):
    initial_investment: float = Field(
        default=None,
        ge=1,
        description="Initial Balance",
    )  ## If not included it just blanks
    ticker_data: Tickers
    risk_profile: RiskProfileModel
    strategies: Strategy
    ta_indicators: TAIndicator

    class Config:
        from_attributes = True
        extra = "forbid"
        title = "Backtest Model"
        description = "Backtest Model"
        json_schema_extra = {
            "example": {
                "initial_investment": 100.0,
                "ticker_data": {
                    "ticker": "AAPL",
                    "date_from": "2021-01-01",
                    "date_to": "2021-12-31",
                },
                "risk_profile": {"risk_level": "medium"},
                "strategies": {"strategy": "greedy"},
                "ta_indicators": {"moving_average": 30, "rsi": 14},
            }
        }
