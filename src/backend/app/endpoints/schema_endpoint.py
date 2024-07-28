from app.models import backtest
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.models import models


router = APIRouter()


@router.get("/ticker", status_code=200, response_model=models.Tickers)
def ticker_model() -> models.Tickers:
    schema = models.Tickers.schema()
    return JSONResponse(content=schema, status_code=200)


@router.get("/ta", status_code=200, response_model=backtest.RiskProfileModel)
def technical_indicator() -> backtest.TAIndicator:
    schema = backtest.TAIndicator.model_json_schema()
    return JSONResponse(content=schema, status_code=200)


@router.get("/risk_level", status_code=200, response_model=backtest.RiskProfileModel)
def risk_level() -> backtest.RiskProfileModel:
    schema = backtest.RiskProfileModel.schema()
    return JSONResponse(content=schema, status_code=200)


@router.get("/strategies", status_code=200, response_model=backtest.Strategy)
def strategies() -> backtest.Strategy:
    schema = backtest.Strategy.schema()
    return JSONResponse(content=schema, status_code=200)
