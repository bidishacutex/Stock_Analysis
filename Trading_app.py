import streamlit as st

st.set_page_config(
    page_title = "Trading App",
    page_icon = "bar_chart:",
    layout = "wide"
)

st.title("CAPM & Stock Prediction System :chart_with_upwards_trend:")

st.header("A Comprehensive Platform for Data-Driven Investment Decisions in Indian and US Stock Markets")

st.image("app.jpg")

st.markdown("## Key Features & Services")

st.markdown("#### :one: Indian & US Stock Market Analysis")
st.write(
    "Gain insights into historical stock data, including trends, key financial indicators, and market behavior. "
    "Analyze both Indian and US stock markets to support informed and diversified investment strategies."
)

st.markdown("#### :two: Indian Stock Price Prediction")
st.write(
    "Get dedicated stock price predictions for Indian stocks. "
    "Forecast future closing prices for the next 30 days based on historical data and advanced machine learning models. "
    "This feature empowers investors focusing on Indian equity markets to make proactive and informed investment decisions."
)

st.markdown("#### :three: US Stock Price Prediction")
st.write(
    "Predict closing prices of US stocks with the same robust forecasting techniques. "
    "Make data-driven decisions while investing in US markets."
)

st.markdown("#### :four: CAPM Expected Return Analysis")
st.write(
    "Calculate the expected return of a stock using the Capital Asset Pricing Model (CAPM) for both Indian and US equities. "
    "Understand the relationship between systematic risk and expected return to optimize your portfolio."
)

st.markdown("#### :five: CAPM Beta Analysis")
st.write(
    "Explore the Beta value of Indian and US stocks to evaluate their volatility relative to the market. "
    "Assess the risk level of your investments and adjust your strategies accordingly."
)