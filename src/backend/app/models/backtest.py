from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from app.models.db_models import TickersModel
from enum import Enum
from pydantic import BaseModel


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


class StrategyLevel(Enum):
    GREEDY = "greedy"
    RANDOM = "random"


class Strategy(BaseModel):
    strategy: StrategyLevel = Field(
        default=StrategyLevel.GREEDY, description="Strategy Level"
    )


class BacktestModel(BaseModel):
    ticker_data: TickersModel
    risk_profile: RiskProfileModel
    strategies: Strategy
    ta_indicators: TAIndicator
