import pandas as pd
from app.models.backtest import BacktestModel, RiskLevel
from typing import Tuple
import vectorbt as vbt
import json


async def digest_data(backtest: BacktestModel) -> pd.DataFrame:
    safe_rsi, neutral_rsi, risky_rsi = 1.5, 2, 2.5
    sma_safe, sma_neutral, sma_risky = 4, 3, 2
    safe_stop_loss, neutral_stop_loss, risky_stop_loss = 0.05, 0.1, 0.15
    safe_rsi_lookback, neutral_rsi_lookback, risky_rsi_lookback = 28, 21, 14
    # tuple is returned as RSI, SMA, Stop_loss
    if backtest.risk_profile.risk_level == RiskLevel.LOW:
        values = (safe_rsi, sma_safe, safe_stop_loss, safe_rsi_lookback)
    elif backtest.risk_profile.risk_level == RiskLevel.MEDIUM:
        values = (neutral_rsi, sma_neutral, neutral_stop_loss, neutral_rsi_lookback)
    elif backtest.risk_profile.risk_level == RiskLevel.HIGH:
        values = (risky_rsi, sma_risky, risky_stop_loss, risky_rsi_lookback)

    return values


async def implement_strategy(
    df: pd.DataFrame, backtest: BacktestModel
) -> Tuple[pd.Series, vbt.utils.figure.Figure]:
    """
    Can be processed in parralel if I did strategy object but no noeed since it is small dataset
    Implement the strategy on the stock data and return a graph of the results
    """
    df = df.copy()

    rsi_threshold, risk_sma_multiplier, stop_loss, rsi_lookback = await digest_data(
        backtest
    )

    rsi_anchor = backtest.ta_indicators.rsi
    sma_lookback = backtest.ta_indicators.moving_average

    price = df.get("Close")
    fast_ma = vbt.MA.run(price, window=sma_lookback)
    slow_ma = vbt.MA.run(price, window=(sma_lookback * risk_sma_multiplier))

    rsi = vbt.RSI.run(price, window=rsi_lookback)

    entries = fast_ma.ma_crossed_above(slow_ma) | rsi.rsi_below(rsi_anchor)
    exits = fast_ma.ma_crossed_below(slow_ma) | rsi.rsi_above(
        rsi_anchor * rsi_threshold
    )

    pf = vbt.Portfolio.from_signals(
        close=price,
        entries=entries,
        exits=exits,
        init_cash=backtest.initial_investment,
        fees=0.002,
        sl_stop=stop_loss,
    )

    chart = pf.plot().to_json()
    chart = json.dumps(chart)
    return pf.stats().to_json(), chart
