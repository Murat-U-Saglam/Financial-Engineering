from pydantic import BaseModel, Field


class BlackScholesCalculator(BaseModel):
    spot_price: float = Field(
        default=100.0,
        ge=1,
        description="Current Price of the stock",
    )
    strike_price: float = Field(
        default=120.0, ge=1, description="Strike Price of the Option"
    )
    time_to_maturity: float = Field(
        default=1.0, ge=0, description="Time to Maturity in Years"
    )
    volatility: float = Field(default=0.2, ge=0, description="Volatility of the stock")
    risk_free_rate: float = Field(default=0.05, ge=0, description="Risk Free Rate")


class BlackScholesCalculatorFromTicker(BaseModel):
    ticker: str = Field(
        default="AAPL", max_length=10, description="Ticker of the stock"
    )
    strike_price: float = Field(
        default=100.0,
        ge=1,
        description="Current Price of the stock",
    )
    time_to_maturity: float = Field(
        default=1.0, ge=0, description="Time to Maturity in Years"
    )
    risk_free_rate: float = Field(default=0.05, ge=0, description="Risk Free Rate")
