from pydantic import BaseModel, Field, PastDate
from enum import Enum
import datetime as dt
from dateutil.relativedelta import relativedelta
from app.models.SQLModel import Tickers


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
        default=30,
        ge=1,
        le=100,
        description="Relative Strength Index - Moving Average length",
    )


class BacktestModel(BaseModel):
    initial_investment: float = Field(
        default=100,
        ge=1,
        description="Initial Balance",
    )  ## If not included it just blanks
    ticker_data: Tickers
    risk_profile: RiskProfileModel
    ta_indicators: TAIndicator

    class Config:
        from_attributes = True
        extra = "forbid"
        title = "Backtest Model"
        description = "Backtest Model"
