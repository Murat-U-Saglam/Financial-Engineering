from backend.models.backtest import BacktestModel
from backend.backtest.strategy import implement_strategy
from typing import Dict
from backend.db.inbound_data import get_stock_data_from_api


async def process_backtest(backtest: BacktestModel) -> tuple[Dict, Dict]:
    try:
        backtest.model_validate(backtest)
    finally:
        pass
    df = await get_stock_data_from_api(backtest.ticker_data)
    meta_data, graph = await implement_strategy(df=df, backtest=backtest)
    return (meta_data, graph)
