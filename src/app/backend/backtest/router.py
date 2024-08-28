from backend.models.backtest import BacktestModel
from backend.backtest.behaviour import process_backtest
from . import logger


async def get_backtest(backtest: BacktestModel):
    logger.error(f"Received backtest request for {backtest}")
    stats = await process_backtest(backtest=backtest)
    return stats
