from fastapi import APIRouter, HTTPException

from app.models.blackschole import (
    BlackScholesCalculator,
    BlackScholesCalculatorFromTicker,
)
from app.blackscholescalculator.behaviour import (
    visualise_black_scholes_in_3d,
    calculate_black_scholes_from_ticker,
)
from fastapi import Depends
import json
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_session


router = APIRouter()


@router.post("/visualise", status_code=200, response_model=str)
async def calculate_black_scholes(black_scholes: BlackScholesCalculator):
    try:
        data = await visualise_black_scholes_in_3d(data=black_scholes)
        chart = data.to_json()
        chart = json.dumps(chart)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return chart


@router.post(path="/calculate_from_ticker", status_code=200, response_model=str)
async def calculate_from_ticker(
    data: BlackScholesCalculatorFromTicker,
    session: AsyncSession = Depends(dependency=get_session),
):
    try:
        spot_price, volatility = await calculate_black_scholes_from_ticker(
            ticker=data.ticker, session=session
        )
        data = BlackScholesCalculator(
            spot_price=spot_price,
            volatility=volatility,
            strike_price=data.strike_price,
            risk_free_rate=data.risk_free_rate,
            time_to_maturity=data.time_to_maturity,
        )
        chart = await visualise_black_scholes_in_3d(data=data)
        chart = chart.to_json()
        chart = json.dumps(chart)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return chart
