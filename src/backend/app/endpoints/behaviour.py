from app.models.backtest import BacktestModel
from pydantic import ValidationError
from fastapi import HTTPException, Depends
from pandas import DataFrame
from app.data.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from app.data.utils import create_ticker_and_stock, get_stock_data_by_ticker
from app.backtest.strategy import implement_strategy

async def process_backtest(
    backtest: BacktestModel, session: AsyncSession = Depends(dependency=get_session)
) -> DataFrame:
    try:
        backtest.model_validate(backtest)
    except ValidationError as e:
        raise HTTPException(status_code=404, detail=e.errors())

    await create_ticker_and_stock(backtest.ticker_data, session=session)
    df = await get_stock_data_by_ticker(backtest.ticker_data, session=session)
    graph = await implement_strategy(df, backtest)

    return df
