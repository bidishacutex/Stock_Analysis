import streamlit as st
import pandas as pd
from pages.utils.model_train import get_data, get_rolling_mean, get_differencing_order, scaling, evaluate_model, get_forecast, inverse_scaling
from pages.utils.plotly_figure import plotly_table, Moving_average_forecast

# Streamlit page configuration
st.set_page_config(
    page_title="Stock Prediction",
    page_icon="chart_with_downwards_trend:",
    layout="wide"
)

st.title("Stock Prediction")

# Columns layout
col1, col2, col3 = st.columns(3)

with col1:
    ticker = st.text_input('Stock Ticker', 'AAPL')

# Initialize RMSE
rmse = 0

# Subheader for prediction info
st.subheader(f'Predicting Next 30 Days Close Price for: {ticker}')

# Step 1: Get stock data
close_price = get_data(ticker)

# Step 2: Rolling mean (Moving Average)
rolling_price = get_rolling_mean(close_price)

# Step 3: Differencing order for stationarity
differencing_order = get_differencing_order(rolling_price)

# Step 4: Scale the data
scaled_data, scaler = scaling(rolling_price)

# Step 5: Evaluate the model
rmse = evaluate_model(scaled_data, differencing_order)
st.write("Model RMSE Score:", rmse)

# Step 6: Get forecast
forecast = get_forecast(scaled_data, differencing_order)

# Step 7: Inverse scaling
forecast['Close'] = inverse_scaling(scaler, forecast['Close'])

# Step 8: Display forecast data
st.write('##### Forecast Data (Next 30 Days)')
fig_tail = plotly_table(forecast.sort_index(ascending=True).round(3))
fig_tail.update_layout(height=220)
st.plotly_chart(fig_tail, use_container_width=True)

# Step 9: Combine rolling_price and forecast for plotting
combined_forecast = pd.concat((rolling_price, forecast))

# Step 10: Plot moving average forecast
st.plotly_chart(Moving_average_forecast(combined_forecast.iloc[-150:]), use_container_width=True)
