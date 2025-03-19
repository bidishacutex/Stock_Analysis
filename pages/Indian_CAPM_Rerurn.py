import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import capm_functions_india  # Assuming you have interactive_plot, normalize, daily_return, calculate_beta here

# Page Configuration
st.set_page_config(page_title="CAPM Return India",
                   page_icon="📈",
                   layout="wide",
                   initial_sidebar_state="auto")

st.title("Capital Asset Pricing Model - Indian Stocks")

# Default Indian Stocks List
default_stocks = ["RELIANCE.NS", "INFY.NS", "HDFCBANK.NS", "TCS.NS", "ICICIBANK.NS", "SBIN.NS", "LT.NS"]

# User Inputs
col1, col2, col3 = st.columns(3)

with col1:
    stock_input = st.text_area("Enter Indian stock symbols separated by commas:", ",".join(default_stocks))
    stock_options = [stock.strip().upper() for stock in stock_input.split(',') if stock.strip()]

    if len(stock_options) < 4:
        st.warning("At least 4 stock symbols are required. Using default stocks.")
        stock_options = default_stocks

with col2:
    default_selection = stock_options[:4] if len(stock_options) >= 4 else default_stocks[:4]
    stocks_list = st.multiselect("Choose exactly 4 stocks:", stock_options, default=default_selection)

    if len(stocks_list) != 4:
        st.error("You must select exactly 4 stocks.")

with col3:
    year = st.number_input("Number of Years:", min_value=1, max_value=10)

# Date Range for Data Download
end = datetime.date.today()
start = datetime.date(end.year - year, end.month, end.day)

# ===========================
# Downloading Stock Data
# ===========================
stocks_df = None  # Initialize

for stock in stocks_list:
    data = yf.download(stock, start=start, end=end)

    if data.empty:
        st.warning(f"No data found for {stock}. Skipping.")
        continue

    # Keep only Date and Close prices, and rename Close column
    data = data[['Close']].reset_index()

    # Convert Date to date only (no time)
    data['Date'] = pd.to_datetime(data['Date']).dt.date

    data.rename(columns={'Close': stock}, inplace=True)

    if stocks_df is None:
        stocks_df = data
    else:
        stocks_df = pd.merge(stocks_df, data, on='Date', how='outer')

# Finalize stocks_df
if stocks_df is None:
    st.error("No valid stock data downloaded. Please check your inputs.")
    st.stop()

# Sort by Date, fill missing values, reset index
stocks_df.sort_values('Date', inplace=True)
stocks_df.fillna(method='ffill', inplace=True)
stocks_df.reset_index(drop=True, inplace=True)

# ===========================
# Download Nifty 50 Data
# ===========================
nifty_df = yf.download('^NSEI', start=start, end=end)

if not nifty_df.empty:
    nifty_df = nifty_df[['Close']].reset_index()

    # Convert Date to date only (no time)
    nifty_df['Date'] = pd.to_datetime(nifty_df['Date']).dt.date

    nifty_df.rename(columns={'Close': 'Nifty50'}, inplace=True)

    # Merge with stocks_df on Date
    merged_df = pd.merge(stocks_df, nifty_df, on='Date', how='inner')
else:
    st.warning("No Nifty 50 data found in the selected date range.")
    merged_df = stocks_df.copy()

# ===========================
# Flatten Column Names to Remove MultiIndex
# ===========================
merged_df.columns = [col if isinstance(col, str) else col[0] for col in merged_df.columns]


# ===========================
# Display DataFrame Head/Tail
# ===========================
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Dataframe Head")
    st.dataframe(merged_df.head(), use_container_width=True)

with col2:
    st.markdown("### Dataframe Tail")
    st.dataframe(merged_df.tail(), use_container_width=True)

# ===========================
# Plots
# ===========================
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Price of All the Stocks")
    st.plotly_chart(capm_functions_india.interactive_plot(merged_df), use_container_width=True)

with col2:
    st.markdown("### Price of all the Stocks (After Normalizing)")
    normalized_df = capm_functions_india.normalize(merged_df)
    st.plotly_chart(capm_functions_india.interactive_plot(normalized_df), use_container_width=True)

# Calculate daily returns for merged data (includes Nifty50)
stocks_daily_return = capm_functions_india.daily_return(merged_df)

# Initialize beta and alpha dictionaries
beta = {}
alpha = {}

# Calculate beta and alpha for each stock (relative to Nifty50)
for i in stocks_daily_return.columns:
    if i != 'Date' and i != 'Nifty50':  # Exclude Date and Nifty50 (market index)
        b, a = capm_functions_india.calculate_beta(stocks_daily_return, i, market='Nifty50')
        beta[i] = b
        alpha[i] = a


# Create Beta DataFrame
beta_df = pd.DataFrame({
    'Stock': list(beta.keys()),
    'Beta Value': [round(val, 2) for val in beta.values()]
})

# CAPM Calculated Return Values
col1, col2 = st.columns(2)

with col1:
    st.markdown('### Calculated Beta Values')
    st.dataframe(beta_df, use_container_width=True)

# Risk-Free Rate for India (adjust as per current data)
rf = 0  # Example: 7% risk-free rate (India 10-year bond yield)

# Calculate Market Return (Nifty50)
rm = stocks_daily_return['Nifty50'].mean() * 252  # Annualized average return of Nifty50

# Calculate Expected Return for Each Stock using CAPM
return_value = []

for stock, b in beta.items():
    capm_return = rf + b * (rm - rf)
    return_value.append(round(capm_return, 2))

# Create Return DataFrame
return_df = pd.DataFrame({
    'Stock': list(beta.keys()),
    'Expected Return (CAPM)': return_value
})

with col2:
    st.markdown('### Calculated Return using CAPM (India)')
    st.dataframe(return_df, use_container_width=True)

