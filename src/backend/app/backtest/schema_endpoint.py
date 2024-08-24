from app.models import backtest
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.models.blackschole import (
    BlackScholesCalculator,
    BlackScholesCalculatorFromTicker,
)



router = APIRouter()


@router.get("/ticker", status_code=200, response_model=backtest.Tickers)
async def ticker_model() -> JSONResponse:
    schema = backtest.Tickers.schema()
    return JSONResponse(content=schema, status_code=200)


@router.get("/ta", status_code=200, response_model=backtest.RiskProfileModel)
async def technical_indicator() -> JSONResponse:
    schema = backtest.TAIndicator.model_json_schema()
    return JSONResponse(content=schema, status_code=200)


@router.get("/risk_level", status_code=200, response_model=backtest.RiskProfileModel)
async def risk_level() -> JSONResponse:
    schema = backtest.RiskProfileModel.schema()
    return JSONResponse(content=schema, status_code=200)


@router.get("/blackscholes", status_code=200, response_model=BlackScholesCalculator)
async def blackscholes() -> JSONResponse:
    schema = BlackScholesCalculator.schema()
    return JSONResponse(content=schema, status_code=200)


@router.get(
    path="/blackscholes_from_ticker",
    status_code=200,
    response_model=BlackScholesCalculatorFromTicker,
)
async def blackscholes_from_ticker() -> JSONResponse:
    schema = BlackScholesCalculatorFromTicker.schema()
    return JSONResponse(content=schema, status_code=200)
