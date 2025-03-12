import streamlit as st

st.set_page_config(
    page_title = "Trading App",
    page_icon = "bar_chart:",
    layout = "wide"
)

st.title("Trading Guide App :chart_with_upwards_trend:")

st.header("We provide the Greatest platform for you to collect all information prior to investing in stocks.")

st.image("app.jpg")

st.markdown("## We provide the following services:")

st.markdown("#### :one: Stock Information")
st.write("Through this page, you can see all the information about stock. ")

st.markdown("#### :two: Stock Prediction")
st.write("You can explore the predicted closing prices for the next 30 days based on historical stock data and advanced forecasting techniques, helping you make informed investment decisions.")

st.markdown("#### :three: CAPM Return")
st.write("You can explore the expected return of a stock based on the CAPM model, which uses historical data and market risk factors to estimate potential investment returns.")

st.markdown("#### :four: CAPM Beta")
st.write("You can explore the CAPM Beta value, which shows how much a stock is expected to move compared to the overall market, helping you understand its risk level and volatility.")
