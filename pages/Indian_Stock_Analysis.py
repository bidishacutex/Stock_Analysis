import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import datetime
import ta
from pages.utils.plotly_figure import plotly_table
from pages.utils.plotly_figure import filter_data
from pages.utils.plotly_figure import close_chart
from pages.utils.plotly_figure import candlestick
from pages.utils.plotly_figure import Moving_average
from pages.utils.plotly_figure import RSI
from pages.utils.plotly_figure import MACD

# Page configuration
st.set_page_config(page_title="Indian Stock Analysis",
                   page_icon="rupee:",
                   layout="wide",
                   initial_sidebar_state="auto")

st.title("Indian Stock Analysis ")

# Available Indian Indices (Optional: Expand)
indian_indices = {
    'Nifty 50': '^NSEI',
    'Sensex': '^BSESN',
}

# Column Layout
col1, col2, col3 = st.columns(3)

today = datetime.date.today()

# User Inputs
with col1:
    ticker = st.text_input("Stock Ticker", "RELIANCE.NS")

with col2:
    start_date = st.date_input("Choose Start Date", datetime.date(today.year-1, today.month, today.day))

with col3:
    end_date = st.date_input("Choose End Date", datetime.date(today.year, today.month, today.day))

# Stock Info
st.subheader(ticker)

try:
    stock = yf.Ticker(ticker)
    info = stock.info

    st.write(info.get('longBusinessSummary', 'No Description Available'))
    st.write("**Sector:**", info.get('sector', 'N/A'))
    st.write("**Full Time Employees:**", info.get('fullTimeEmployees', 'N/A'))
    st.write("**Website:**", info.get('website', 'N/A'))

    # Display Key Stats
    col1, col2 = st.columns(2)

    with col1:
        df = pd.DataFrame(index=['Market Cap', 'Beta', 'EPS', 'PE Ratio'])
        df[''] = [
            info.get('marketCap', 'N/A'),
            info.get('beta', 'N/A'),
            info.get('trailingEps', 'N/A'),
            info.get('trailingPE', 'N/A')
        ]
        fig_df = plotly_table(df)
        st.plotly_chart(fig_df, use_container_width=True)

    with col2:
        df = pd.DataFrame(index=['Quick Ratio', 'Revenue per Share', 'Profit Margins',
                                 'Debt to Equity', 'Return on Equity'])
        df[''] = [
            info.get('quickRatio', 'N/A'),
            info.get('revenuePerShare', 'N/A'),
            info.get('profitMargins', 'N/A'),
            info.get('debtToEquity', 'N/A'),
            info.get('returnOnEquity', 'N/A')
        ]
        fig_df = plotly_table(df)
        st.plotly_chart(fig_df, use_container_width=True)

except Exception as e:
    st.error(f"Failed to fetch info for {ticker}: {e}")

# Download Historical Data
data = yf.download(ticker, start=start_date, end=end_date)

# Price Change Metric
col1, col2, col3 = st.columns(3)

if len(data) >= 2:
    latest_close = data['Close'].iloc[-1]
    previous_close = data['Close'].iloc[-2]

    daily_change = latest_close - previous_close
    daily_change_percent = (daily_change / previous_close) * 100

    # Ensure it's a float, not Series
    latest_close_value = round(float(latest_close), 2)
    daily_change_percent_value = round(float(daily_change_percent), 2)

    col1.metric(
        label="Daily Change",
        value=f"{latest_close_value}",                # e.g., 222.87
        delta=f"{daily_change_percent_value}%",       # e.g., 14.8%
        delta_color="normal"
    )

elif len(data) == 1:
    latest_close = data['Close'].iloc[-1]

    col1.metric(
        label="Daily Change",
        value=f"{round(float(latest_close), 2)}",
        delta="No previous data"
    )

else:
    col1.metric(
        label="Daily Change",
        value="No data",
        delta="-"
    )


# Last 10 Days Historical Data
if not data.empty:
    last_10_df = data.tail(10).sort_index(ascending=False).round(3)

    # Flatten MultiIndex columns if they exist
    if isinstance(last_10_df.columns, pd.MultiIndex):
        last_10_df.columns = ['_'.join(map(str, col)).strip() for col in last_10_df.columns]
    else:
        last_10_df.columns = [str(col) for col in last_10_df.columns]

    last_10_df.index = last_10_df.index.strftime('%Y-%m-%d')

    fig_df = plotly_table(last_10_df)
    st.subheader(f'Historical Data (Last 10 Days) for {ticker}')
    st.plotly_chart(fig_df, use_container_width=True)

else:
    st.warning("No historical data available for the selected date range.")



# Columns for period selection
col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12 = st.columns(12)

# Initialize num_period
num_period = '1y'  # Set default period as 1y

with col1:
    if st.button('5D'):
        num_period = '5d'
with col2:
    if st.button('6M'):
        num_period = '6mo'
with col3:
    if st.button('YTD'):
        num_period = 'ytd'
with col4:
    if st.button('1Y'):
        num_period = '1y'
with col5:
    if st.button('5Y'):
        num_period = '5y'
with col6:
    if st.button('MAX'):
        num_period = 'max'

# Chart type and indicators selection
col1, col2, col3 = st.columns([1, 1, 4])

with col1:
    chart_type = st.selectbox('Chart Type', ('Candle', 'Line'))

with col2:
    if chart_type == 'Candle':
        indicators = st.selectbox('Indicators', ('RSI', 'MACD'))
    else:
        indicators = st.selectbox('Indicators', ('RSI', 'Moving Average', 'MACD'))

# Ticker input
ticker = st.text_input('Enter ticker:', value=ticker)  # Default ticker for testing

# Fetch data
ticker_obj = yf.Ticker(ticker)
data = ticker_obj.history(period='max')

# Logic for displaying charts
if chart_type == 'Candle':
    if indicators == 'RSI':
        st.plotly_chart(candlestick(data, num_period), use_container_width=True)
        st.plotly_chart(RSI(data, num_period), use_container_width=True)

    elif indicators == 'MACD':
        st.plotly_chart(candlestick(data, num_period), use_container_width=True)
        st.plotly_chart(MACD(data, num_period), use_container_width=True)

elif chart_type == 'Line':
    if indicators == 'RSI':
        st.plotly_chart(close_chart(data, num_period), use_container_width=True)
        st.plotly_chart(RSI(data, num_period), use_container_width=True)

    elif indicators == 'Moving Average':
        st.plotly_chart(Moving_average(data, num_period), use_container_width=True)

    elif indicators == 'MACD':
        st.plotly_chart(close_chart(data, num_period), use_container_width=True)
        st.plotly_chart(MACD(data, num_period), use_container_width=True)

