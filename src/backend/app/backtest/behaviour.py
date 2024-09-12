from app.models.backtest import BacktestModel
from pydantic import ValidationError
from fastapi import HTTPException, Depends
from app.db.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.utils import create_ticker_and_stock, get_stock_data_by_ticker
from app.backtest.strategy import implement_strategy
from typing import Dict


async def process_backtest(
    backtest: BacktestModel, session: AsyncSession = Depends(dependency=get_session)
) -> tuple[Dict, Dict]:
    try:
        backtest.model_validate(backtest)
    except ValidationError as e:
        raise HTTPException(status_code=404, detail=e.errors())
    await create_ticker_and_stock(ticker_model=backtest.ticker_data, session=session)
    df = await session.run_sync(
        fn=get_stock_data_by_ticker, ticker_model=backtest.ticker_data
    )
    meta_data, graph = await implement_strategy(df=df, backtest=backtest)
    return (meta_data, graph)
