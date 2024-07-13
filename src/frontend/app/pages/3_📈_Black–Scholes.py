import streamlit as st

st.title("Black-Scholes Option Pricing Model")
st.write("This is the Black-Scholes Option Pricing Model page.")


input_data = {
    "Current Asset Price": [st.number_input("Current Asset Price", value=100.0)],
    "Strike Price": [st.number_input("Strike Price", value=100.0)],
    "Time to Maturity (Years)": [
        st.number_input("Time to Maturity (Years)", value=1.0)
    ],
    "Volatility (σ)": [st.number_input("Volatility (σ)", value=0.2)],
    "Risk-Free Interest Rate": [st.number_input("Risk-Free Interest Rate", value=0.05)],
}
