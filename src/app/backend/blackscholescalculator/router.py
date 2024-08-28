from backend.models.blackschole import (
    BlackScholesCalculator,
    BlackScholesCalculatorFromTicker,
)
from backend.blackscholescalculator.behaviour import (
    visualise_black_scholes_in_3d,
    calculate_black_scholes_from_ticker,
)
import json


async def calculate_black_scholes(black_scholes: BlackScholesCalculator):
    try:
        data = await visualise_black_scholes_in_3d(data=black_scholes)
        chart = data.to_json()
        chart = json.dumps(chart)
    except Exception as e:
        raise ValueError(str(e))
    return chart


async def calculate_from_ticker(
    data: BlackScholesCalculatorFromTicker,
):
    try:
        spot_price, volatility = await calculate_black_scholes_from_ticker(
            ticker=data.ticker
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
        raise ValueError(str(e))
    return chart
