import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm
from app.models.blackschole import BlackScholesCalculator
from app.db.utils import create_ticker_and_stock, get_stock_data_by_ticker
from app.db.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.SQLModel import Tickers
from fastapi import Depends
import pandas as pd


async def get_latest_price(df: pd.DataFrame) -> float:
    return df["Close"].iloc[-1]


async def calculate_historical_volatility(df: pd.DataFrame) -> float:
    return np.std(
        np.log(np.array(df["Close"][:-1]) / np.array(df["Close"][1:]))
    ) * np.sqrt(len(df))


async def calculate_black_scholes_from_ticker(
    ticker: str, session: AsyncSession = Depends(dependency=get_session)
) -> tuple[float, float]:
    ticker = Tickers(ticker=ticker)
    await create_ticker_and_stock(ticker_model=ticker, session=session)
    df = await session.run_sync(get_stock_data_by_ticker, ticker)
    spot_price = await get_latest_price(df)
    volatility = await calculate_historical_volatility(df)
    return (spot_price, volatility)


async def black_scholes_call(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)


async def black_scholes_delta(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)


async def visualise_black_scholes_in_3d(data: BlackScholesCalculator):
    # Create a range of spot prices and times to maturity
    spot_prices = np.linspace(data.spot_price * 0.5, data.spot_price * 1.5, 50)
    times_to_maturity = np.linspace(0.1, data.time_to_maturity * 1.5, 50)

    # Create meshgrid
    S, T = np.meshgrid(spot_prices, times_to_maturity)

    # Calculate option prices and deltas
    option_prices = await black_scholes_call(
        S, data.strike_price, T, data.risk_free_rate, data.volatility
    )
    option_deltas = await black_scholes_delta(
        S, data.strike_price, T, data.risk_free_rate, data.volatility
    )

    # Create color scale based on delta
    colorscale = [[0, "green"], [0.5, "yellow"], [1, "red"]]

    # Create 3D surface plot
    fig = go.Figure(
        data=[
            go.Surface(
                z=option_prices,
                x=S,
                y=T,
                colorscale=colorscale,
                surfacecolor=option_deltas,
            )
        ]
    )

    # Update layout
    fig.update_layout(
        title="Black-Scholes Option Pricing Model with Risk Visualization",
        scene=dict(
            xaxis_title="Spot Price",
            yaxis_title="Time to Maturity",
            zaxis_title="Option Price",
        ),
    )

    # Add color bar
    fig.update_traces(
        colorbar_title="Delta<br>(Risk Measure)",
        hovertemplate="<b>Spot Price</b>: $%{x:.2f}<br>"
        "<b>Time to Maturity</b>: %{y:.2f} years<br>"
        "<b>Option Price</b>: $%{z:.2f}<br>"
        "<b>Delta</b>: %{surfacecolor:.2f}<extra></extra>",
    )

    return fig
