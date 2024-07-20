import streamlit as st
import httpx
import datetime as dt

st.set_page_config(layout="wide")

st.title(body="Backtest")


def fetch_schema(uri_endpoint: str, full_response: bool = False):
    url = f"http://backend:8001/{uri_endpoint}"
    response = httpx.get(url)
    assert response.status_code == 200, f"Failed to fetch schema from {url}"
    if full_response:
        return response.json()
    return response.json()["properties"]


def run_backtest_endpoint(uri_endpoint: str, body: dict):
    url = f"http://backend:8001/{uri_endpoint}"
    response = httpx.post(url=url, json=body)
    assert response.status_code == 200, f"Failed to run backtest from {url}"
    return response.json()


uri = "schema/ta"
dict_schema = fetch_schema(uri_endpoint=uri)

uri = "schema/ticker"
ticker_inputs = fetch_schema(uri_endpoint=uri)

uri = "schema/risk_level"
risk_profile = fetch_schema(uri_endpoint=uri, full_response=True)

uri = "schema/strategies"
strategies = fetch_schema(uri_endpoint=uri, full_response=True)

columns = st.columns(3)

with columns[0]:
    st.subheader("Ticker Data", divider="grey")
    ticker = st.text_input("Ticker", value=ticker_inputs["ticker"]["default"], max_chars=5)
    micro_column = st.columns(2)
    with micro_column[0]:
        start_date = st.date_input(
            label="Start Date",
            value=dt.datetime.strptime(
                ticker_inputs["date_from"]["default"], "%Y-%m-%d"
            ).date(),
            format="DD/MM/YYYY",
        )
    with micro_column[1]:
        end_date = st.date_input(
            label="End Date",
            value=dt.datetime.strptime(
                ticker_inputs["date_to"]["default"], "%Y-%m-%d"
            ).date(),
            format="DD/MM/YYYY",
        )
    assert start_date < end_date, "Start Date must be before End Date"
    initial_investment = st.number_input(
        label="Initial Investment",
        value=100, min_value=1, max_value=1000000, step=1
    )
    
    assert initial_investment >= 1, "Initial Investment must be greater than 0"

with columns[1]:
    st.subheader(body="TA Indicators", divider="grey")
    moving_average = st.slider(label="Moving Average", min_value=dict_schema["moving_average"]["minimum"], max_value=dict_schema["moving_average"]["maximum"], value=dict_schema["moving_average"]["default"], key="moving_average")
    rsi = st.slider(label="RSI", min_value=dict_schema["rsi"]["minimum"], max_value=dict_schema["rsi"]["maximum"], value=dict_schema["rsi"]["default"], key="rsi" )

with columns[2]:
    st.subheader(body="Risk Profile", divider="grey")
    risk_level = st.selectbox(
        label="Risk Level", options=risk_profile["$defs"]["RiskLevel"]["enum"], index=1
    )
    st.subheader(body="Strategy", divider="grey")
    strategy = st.selectbox(
        label="Strategy", options=strategies["$defs"]["StrategyLevel"]["enum"], index=0
    )


def run_backtest(ticker: str, start_date: dt.datetime, end_date: dt.datetime, risk_level: str, strategy: str, moving_average: int, rsi: int):
    ticker_data = {
        "ticker": ticker,
        "date_from": start_date.strftime("%Y-%m-%d"),
        "date_to": end_date.strftime("%Y-%m-%d")
    }
    risk_profile = {
        "risk_level": risk_level
    }
    strategies = {
        "strategy": strategy
    }
    ta_indicators = {
        "moving_average": moving_average,
        "rsi": rsi
    }
    
    request_body = {
        "initial_investment": 1000,
        "ticker_data": ticker_data,
        "risk_profile": risk_profile,
        "strategies": strategies,
        "ta_indicators": ta_indicators
    }
    
    response = run_backtest_endpoint(uri_endpoint="data/backtest", body=request_body)
    st.write("Backtest Running")
    
    return response

if st.button(label="Run Backtest"):
    with st.spinner():
        result = run_backtest(ticker=ticker, start_date=start_date, end_date=end_date, risk_level=risk_level, strategy=strategy, moving_average=moving_average, rsi=rsi)
    st.success(f"Backtest Completed: {result}")


