# importing libraries:

import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_datareader.data as web
import datetime
import capm_functions

st.set_page_config(page_title= "CAPM Return",
                   page_icon= "chart_with_upwards_trend",
                   layout= "wide",
                   initial_sidebar_state= "auto")

st.title("Capital Asset Pricing Model")

# Default stocks list
default_stocks = ["GOOG", "AAPL", "MSFT", "TSLA", "HDB", "INFY", "IBN"]

# getting input from user

col1, col2, col3 = st.columns([1,1,1])

with col1:
    stock_input = st.text_area("Enter stock symbols separated by commas:", ",".join(default_stocks))

    # Processing user input
    stock_options = [stock.strip().upper() for stock in stock_input.split(',') if stock.strip()]

    # If fewer than 4 stocks are provided, fall back to default
    if len(stock_options) < 4:
        st.warning("At least 4 stock symbols are required. Using default stocks.")
        stock_options = default_stocks
with col2:
    # Ensuring the multiselect always has valid defaults
    default_selection = stock_options[:4] if len(stock_options) >= 4 else default_stocks[:4]

    stocks_list = st.multiselect("Choose exactly 4 stocks:", stock_options, default=default_selection)

    # Enforcing exactly 4 selections
    if len(stocks_list) != 4:
        st.error("You must select exactly 4 stocks.")

with col3:
    year = st.number_input("Number of Years:", min_value=1, max_value=10)

# downloading data for SP500
end = datetime.date.today()
start = datetime.date(datetime.date.today().year-year, datetime.date.today().month, datetime.date.today().day)
SP500 = web.DataReader(['sp500'],'fred',start,end)


stocks_df = pd.DataFrame()
for stock in stocks_list:
     data = yf.download(stock, period = f'{year}y')
     stocks_df[f'{stock}'] = data['Close']

stocks_df.reset_index(inplace = True)
SP500.reset_index(inplace = True)
SP500.columns = ['Date', 'sp500']
stocks_df['Date'] = stocks_df['Date'].apply(lambda x:str(x)[:10])
stocks_df['Date'] = pd.to_datetime(stocks_df['Date'])
stocks_df = pd.merge(stocks_df, SP500, on= 'Date', how = 'inner')



col1, col2 = st.columns([1,1])
with col1:
    st.markdown("### Dataframe Head")
    st.dataframe(stocks_df.head(), use_container_width = True)
with col2:
    st.markdown("### Dataframe Tail")
    st.dataframe(stocks_df.tail(), use_container_width = True)


col1, col2 = st.columns([1,1])
with col1:
    st.markdown("### Price of all the Stocks")
    st.plotly_chart(capm_functions.interactive_plot(stocks_df))
with col2:
    st.markdown("### Price of all the Stocks (After Normalizing)")
    st.plotly_chart(capm_functions.interactive_plot(capm_functions.normalize(stocks_df)))

stocks_daily_return = capm_functions.daily_return(stocks_df)

beta = {}
alpha = {}

for i in stocks_daily_return.columns:
    if i != 'Date' and i != 'sp500':
        b, a = capm_functions.calculate_beta(stocks_daily_return, i)

        beta[i] = b
        alpha[i] = a
print(beta, alpha)

beta_df = pd.DataFrame(columns = ['Stock', 'Beta Value'])
beta_df['Stock'] = beta.keys()
beta_df['Beta Value'] = [str(round(i,2)) for i in beta.values()]

col1, col2 = st.columns(2)
with col1:
    st.markdown('### Calculated Beta Value')
    st.dataframe(beta_df, use_container_width= True)

rf = 0
rm = stocks_daily_return['sp500'].mean()*252

return_df = pd.DataFrame()
return_value = []
for stock, value in beta.items():
    return_value.append(str(round(rf+(value*(rm-rf)),2)))
return_df['Stock'] = stocks_list

return_df['Return Value'] = return_value

with col2:
    st.markdown('### Calculated Return using CAPM')
    st.dataframe(return_df, use_container_width= True)