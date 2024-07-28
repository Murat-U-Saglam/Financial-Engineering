from fastapi import APIRouter, Depends
from app.models.backtest import BacktestModel
from app.endpoints.behaviour import process_backtest
from fastapi.responses import JSONResponse
from . import logger
from app.data.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession


router = APIRouter()


@router.post("/backtest", status_code=200)
async def get_backtest(
    backtest: BacktestModel, session: AsyncSession = Depends(dependency=get_session)
):
    logger.info(msg=f"Received backtest request for {backtest}")
    df = await process_backtest(backtest=backtest, session=session)
    logger.error(df)
    return JSONResponse(content=df.dict(), status_code=200)
