import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.title("Stock Market Trend Analysis Dashboard")

stocks = st.multiselect(
    "Select Stocks",
    ["TCS.NS", "INFY.NS", "RELIANCE.NS", "HDFCBANK.NS"],
    default=["TCS.NS"]
)

start_date = st.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.date_input("End Date", pd.to_datetime("2024-01-01"))

if stocks:
    for stock in stocks:
        st.subheader(f"Analysis of {stock}")

        data = yf.download(stock, start=start_date, end=end_date)

        if data.empty:
            st.write("No data available")
            continue

        # ✅ FIX: Flatten MultiIndex columns if present (newer yfinance versions)
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        # Moving average
        data['Average'] = data['Close'].rolling(10).mean()

        st.write(data.tail())

        # ✅ FIX: Use .values to get scalar for comparison
        if data['Close'].values[-1] > data['Close'].values[0]:
            trend = "UP 📈"
        else:
            trend = "DOWN 📉"

        st.write(f"Trend: {trend}")

        fig, ax = plt.subplots()
        ax.plot(data['Close'], label='Price')
        ax.plot(data['Average'], label='10-Day Moving Avg')
        ax.set_title(f"{stock} Price Trend")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price (INR)")
        ax.legend()
        st.pyplot(fig)