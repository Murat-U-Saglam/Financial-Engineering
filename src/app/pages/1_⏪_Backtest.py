import streamlit as st
import datetime as dt
import json
from plotly.io import from_json
import pandas as pd
from backend.models.backtest import RiskLevel, TAIndicator, Tickers, BacktestModel
from backend.backtest.router import get_backtest
import asyncio

st.set_page_config(page_title="Backtest", layout="wide")

st.title(body="Backtest")


async def run_backtest_endpoint(data: dict):
    data = BacktestModel(**data)
    return await get_backtest(backtest=data)


dict_schema = TAIndicator.schema()["properties"]

ticker_inputs = Tickers.schema()["properties"]

risk_profile = [e.value for e in RiskLevel]

columns = st.columns(3)

with columns[0]:
    st.subheader("Ticker Data", divider="grey")
    ticker = st.text_input(
        "Ticker",
        value=ticker_inputs["ticker"]["default"],
        max_chars=ticker_inputs["ticker"]["maxLength"],
    )
    micro_column = st.columns(2)
    with micro_column[0]:
        start_date = st.date_input(
            label="Start Date",
            max_value=dt.datetime.now().date() - dt.timedelta(days=60),
            value=dt.datetime.strptime(
                ticker_inputs["date_from"]["default"], "%Y-%m-%d"
            ).date(),
            format="DD/MM/YYYY",
        )
    with micro_column[1]:
        end_date = st.date_input(
            label="End Date",
            min_value=start_date + dt.timedelta(days=1),
            max_value=dt.datetime.now().date() - dt.timedelta(days=1),
            value=dt.datetime.strptime(
                ticker_inputs["date_to"]["default"],
                "%Y-%m-%d",
            ).date(),
            format="DD/MM/YYYY",
        )


with columns[1]:
    st.subheader(body="TA Indicators", divider="grey")
    moving_average = st.slider(
        label="Moving Average",
        min_value=dict_schema["moving_average"]["minimum"],
        max_value=dict_schema["moving_average"]["maximum"],
        value=dict_schema["moving_average"]["default"],
        key="moving_average",
    )
    rsi = st.slider(
        label="RSI",
        min_value=dict_schema["rsi"]["minimum"],
        max_value=dict_schema["rsi"]["maximum"],
        value=dict_schema["rsi"]["default"],
        key="rsi",
    )

with columns[2]:
    st.subheader(body="Risk Profile", divider="grey")
    risk_level = st.selectbox(label="Risk Level", options=risk_profile, index=1)
    initial_investment = st.number_input(
        label="Initial Investment", value=100, min_value=1, max_value=1000000, step=1
    )


async def run_backtest(
    ticker: str,
    start_date: dt.datetime,
    end_date: dt.datetime,
    risk_level: str,
    moving_average: int,
    rsi: int,
):
    ticker_data = {
        "date_to": end_date.strftime("%Y-%m-%d"),
        "date_from": start_date.strftime("%Y-%m-%d"),
        "ticker": ticker,
    }
    risk_profile = {"risk_level": risk_level}
    ta_indicators = {"moving_average": moving_average, "rsi": rsi}

    request_body = {
        "initial_investment": initial_investment,
        "ticker_data": ticker_data,
        "risk_profile": risk_profile,
        "ta_indicators": ta_indicators,
    }

    response = await run_backtest_endpoint(data=request_body)
    st.write("Backtest Running")

    return response


if st.button(label="Run Backtest"):
    with st.spinner():
        result = asyncio.run(
            run_backtest(
                ticker=ticker,
                start_date=start_date,
                end_date=end_date,
                risk_level=risk_level,
                moving_average=moving_average,
                rsi=rsi,
            )
        )
    data = pd.Series(json.loads(result[0]))
    series = pd.Series(data)
    col1, col2 = st.columns([3, 1])
    chart = json.loads(result[1])
    col1.plotly_chart(figure_or_data=from_json(chart))
    col2.subheader("Backtest Results")
    col2.dataframe(series, height=800)
