# importing libraries:

import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title= "CAPM_Calculate",
                   page_icon= "chart_with_upwards_trend",
                   layout= "wide",
                   initial_sidebar_state= "auto")

st.title("Capital Asset Pricing Model")

# getting input from user

col1, col2 = st.columns([1,1])
with col1:
    stock_list = st.multiselect("choose 4 stock", ('TSLA','AAPL','NFLX','MSFT','MGM','AMZN'), ['TSLA','AAPL','NFLX','MSFT'])
with col2:
    year = st.number_input("Number of Years", 1,10)
