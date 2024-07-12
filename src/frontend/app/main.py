import streamlit as st


st.title("Hello, World!")
st.write("Welcome to your Streamlit app running in a Docker container.")

with st.sidebar:
    st.sidebar.write("Configuration")
    ticker = st.sidebar.text_input(label="Stock Ticker")
    time_delta = st.sidebar.slider(
        label="Time Period in days", min_value=10, max_value=88, value=25, step=1
    )
    st.write(f"Stock Ticker: {ticker}")
    st.write(f"Time Period: {time_delta} days")
    if st.button("Analyse"):
        st.write("Analyzing...")
