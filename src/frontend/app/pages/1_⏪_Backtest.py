import streamlit as st
import httpx
import datetime as dt
import json
from plotly.io import from_json
import pandas as pd

st.set_page_config(page_title="Backtest", layout="wide")

st.title(body="Backtest")


def fetch_schema(uri_endpoint: str, full_response: bool = False):
    url = f"http://backend:8001/{uri_endpoint}"
    response = httpx.get(url, timeout=60)
    if full_response:
        return response.json()
    return response.json()["properties"]


def run_backtest_endpoint(uri_endpoint: str, body: dict):
    url = f"http://backend:8001/{uri_endpoint}"
    response = httpx.post(url=url, json=body, timeout=60)
    if response.status_code != 200:
        st.error(f"Backtest Failed: {response}")
    return response.json()


uri = "schema/ta"
dict_schema = fetch_schema(uri_endpoint=uri)

uri = "schema/ticker"
ticker_inputs = fetch_schema(uri_endpoint=uri)

uri = "schema/risk_level"
risk_profile = fetch_schema(uri_endpoint=uri, full_response=True)


columns = st.columns(3)

with columns[0]:
    st.subheader("Ticker Data", divider="grey")
    ticker = st.text_input(
        "Ticker", value=ticker_inputs["ticker"]["default"], max_chars=5
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
    risk_level = st.selectbox(
        label="Risk Level", options=risk_profile["$defs"]["RiskLevel"]["enum"], index=1
    )
    initial_investment = st.number_input(
        label="Initial Investment", value=100, min_value=1, max_value=1000000, step=1
    )


def run_backtest(
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


    response = run_backtest_endpoint(uri_endpoint="data/backtest", body=request_body)
    st.write("Backtest Running")

    return response


if st.button(label="Run Backtest"):
    with st.spinner():
        result = run_backtest(
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
            risk_level=risk_level,
            moving_average=moving_average,
            rsi=rsi,
        )
    data = pd.Series(json.loads(result[0]))
    series = pd.Series(data)
    col1, col2 = st.columns([3, 1])
    chart = json.loads(result[1])
    col1.plotly_chart(figure_or_data=from_json(chart))
    col2.subheader("Backtest Results")
    col2.dataframe(series, height=800)