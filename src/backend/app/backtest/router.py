from fastapi import APIRouter, Depends
from app.models.backtest import BacktestModel
from app.backtest.behaviour import process_backtest
from . import logger
from app.data.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession


router = APIRouter()


@router.post(path="/backtest", status_code=200)
async def get_backtest(
    backtest: BacktestModel, session: AsyncSession = Depends(dependency=get_session)
):
    logger.error(f"Received backtest request for {backtest}")
    stats = await process_backtest(backtest=backtest, session=session)
    return stats
