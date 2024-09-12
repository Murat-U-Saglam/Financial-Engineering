import streamlit as st
import httpx
import json
from typing import Dict
import plotly
import os

st.set_page_config(layout="wide")

BACKEND_PORT = os.environ.get("BACKEND_PORT", 8001)


def fetch_schema(uri_endpoint: str, full_response: bool = False):
    url = f"http://backend:{BACKEND_PORT}/{uri_endpoint}"
    response = httpx.get(url, timeout=60)
    if full_response:
        return response.json()
    return response.json()["properties"]


def run_visualisation(post_params: Dict[str, int]):
    response = httpx.post(
        f"http://backend:{BACKEND_PORT}/blackscholes/calculate_from_ticker",
        json=post_params,
    )
    if response.status_code != 200:
        st.error(f"Failed to create visualisation: {response}")
    return response.json()


st.title("Black-Scholes Option Pricing Model")
st.write("This is the Black-Scholes Option Pricing Model page.")

schema = fetch_schema(uri_endpoint="schema/blackscholes_from_ticker")
no_of_columns = len(schema)
cols = st.columns(no_of_columns)

with cols[0]:
    ticker = st.text_input(label="Ticker", value=schema["ticker"]["default"])

with cols[1]:
    strike_proce = st.number_input(
        label="Strike price",
        min_value=schema["strike_price"]["minimum"],
        value=schema["strike_price"]["default"],
    )

with cols[2]:
    time_to_maturity = st.number_input(
        label="Time to maturity in Years",
        min_value=schema["time_to_maturity"]["minimum"],
        value=schema["time_to_maturity"]["default"],
    )

with cols[3]:
    interest_rate = st.number_input(
        label="Risk free rate",
        min_value=schema["risk_free_rate"]["minimum"],
        value=schema["risk_free_rate"]["default"],
    )


if st.button(label="Create Visualisation", use_container_width=True):
    with st.spinner(text="Creating Visualisation"):
        post_params = {
            "ticker": ticker,
            "strike_price": strike_proce,
            "time_to_maturity": time_to_maturity,
            "risk_free_rate": interest_rate,
        }
        graph = run_visualisation(post_params=post_params)
    chart = json.loads(graph)
    st.plotly_chart(plotly.io.from_json(chart))
