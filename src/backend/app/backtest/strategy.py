import pandas as pd
from app.models.backtest import BacktestModel
import pandas_ta as ta

async def implement_strategy(df: pd.DataFrame, backtest: BacktestModel) -> pd.DataFrame:
    """
    Can be processed in parralel if I did strategy object but no noeed since it is small dataset
    Implement the strategy on the stock data and return a graph of the results
    """
    # Implement the strategy here
    if backtest.ta_indicators.moving_average:
        df.ta.sma(length=backtest.ta_indicators.moving_average, append=True)
    if backtest.ta_indicators.rsi:
        df.ta.rsi(length=backtest.ta_indicators.rsi, append=True)
    
    return df