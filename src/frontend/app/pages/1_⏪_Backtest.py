import streamlit as st
import httpx
import datetime as dt

st.set_page_config(layout="wide")

st.title(body="Backtest")


def fetch_schema(uri_endpoint: str, full_response: bool = False):
    url = f"http://backend:8001/{uri_endpoint}"
    response = httpx.get(url)
    assert response.status_code == 200
    if full_response:
        return response.json()
    return response.json()["properties"]


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
    st.text_input("Ticker", value=ticker_inputs["ticker"]["default"], max_chars=5)
    st.date_input(
        label="Start Date",
        value=dt.datetime.strptime(
            ticker_inputs["date_from"]["default"], "%Y-%m-%d"
        ).date(),
        format="DD/MM/YYYY",
    )
    st.date_input(
        label="Start Date",
        value=dt.datetime.strptime(
            ticker_inputs["date_to"]["default"], "%Y-%m-%d"
        ).date(),
        format="DD/MM/YYYY",
    )
with columns[1]:
    st.subheader("TA Indicators", divider="grey")

    for key, value in dict_schema.items():
        internal_label = key.replace("_", " ").title()
        st.slider(
            label=internal_label,
            min_value=value["minimum"],
            max_value=value["maximum"],
            value=value["default"],
        )

with columns[2]:
    st.subheader(body="Risk Profile", divider="grey")
    risk_level = st.selectbox(
        label="Risk Level", options=risk_profile["$defs"]["RiskLevel"]["enum"], index=1
    )
    st.subheader(body="Strategy", divider="grey")
    strategy = st.selectbox(
        label="Strategy", options=strategies["$defs"]["StrategyLevel"]["enum"], index=0
    )


st.button(label="Run Backtest", on_click=lambda: st.write("Backtest Running"))
## TODO make a post request to the backend with the data
