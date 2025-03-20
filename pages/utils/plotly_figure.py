import plotly.graph_objects as go
import pandas_ta as pta
import dateutil
import pandas as pd

# ==========================
# FILTER FUNCTION
# ==========================
def filter_data(dataframe, num_period):
    if not isinstance(dataframe.index, pd.DatetimeIndex):
        dataframe.index = pd.to_datetime(dataframe.index)

    # Handle time stripping only if NOT 1d
    if num_period != '1d':
        dataframe.index = dataframe.index.normalize()  # Remove time component

    latest_date = dataframe.index[-1]

    if num_period == '1d':
        date = latest_date - dateutil.relativedelta.relativedelta(days=1)
    elif num_period == '5d':
        date = latest_date - dateutil.relativedelta.relativedelta(days=5)
    elif num_period == '6mo':
        date = latest_date - dateutil.relativedelta.relativedelta(months=6)
    elif num_period == '1y':
        date = latest_date - dateutil.relativedelta.relativedelta(years=1)
    elif num_period == '5y':
        date = latest_date - dateutil.relativedelta.relativedelta(years=5)
    elif num_period == 'ytd':
        date = latest_date.replace(month=1, day=1)
    else:
        date = dataframe.index[0]

    df_filtered = dataframe[dataframe.index > date].copy()

    # Add Date column for plotting
    if num_period == '1d':
        df_filtered['Date'] = df_filtered.index  # keep datetime
    else:
        df_filtered['Date'] = df_filtered.index.date  # date only

    return df_filtered

# ==========================
# TABLE FUNCTION
# ==========================
def plotly_table(dataframe):
    headerColor = 'grey'
    rowEvenColor = '#f8fafd'
    rowOddColor = '#e1efff'

    fill_colors = [
        rowOddColor if i % 2 == 0 else rowEvenColor
        for i in range(len(dataframe))
    ]

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["<b><b>"] + ["<b>" + str(i)[:10] + "<b>" for i in dataframe.columns],
            line_color='#0078ff',
            fill_color='#0078ff',
            align='center',
            font=dict(color='white', size=15),
            height=35
        ),
        cells=dict(
            values=[["<b>" + str(i) + "<b>" for i in dataframe.index]] +
                   [dataframe[i] for i in dataframe.columns],
            line_color='white',
            fill_color=[fill_colors] * len(dataframe.columns),
            align='left',
            font=dict(color='black', size=15)
        )
    )])

    fig.update_layout(height=400, margin=dict(l=0, r=0, t=0, b=0))
    return fig

# ==========================
# CLOSE CHART
# ==========================
def close_chart(dataframe, num_period=False):
    if num_period:
        dataframe = filter_data(dataframe, num_period)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['Open'],
        mode='lines', name='Open', line=dict(width=2, color='#5ab7ff')
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['Close'],
        mode='lines', name='Close', line=dict(width=2, color='black')
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['High'],
        mode='lines', name='High', line=dict(width=2, color='#0078ff')
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['Low'],
        mode='lines', name='Low', line=dict(width=2, color='red')
    ))

    fig.update_xaxes(
        rangeslider_visible=True,
        tickformat="%Y-%m-%d", tickangle=45
    )

    fig.update_layout(
        height=500,
        margin=dict(l=0, r=20, t=20, b=0),
        plot_bgcolor='white',
        paper_bgcolor='#e1efff',
        legend=dict(yanchor="top", xanchor="right")
    )
    return fig

# ==========================
# CANDLESTICK CHART
# ==========================
def candlestick(dataframe, num_period):
    dataframe = filter_data(dataframe, num_period)

    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=dataframe['Date'],
        open=dataframe['Open'],
        high=dataframe['High'],
        low=dataframe['Low'],
        close=dataframe['Close']
    ))

    fig.update_xaxes(
        tickformat="%Y-%m-%d", tickangle=45, rangeslider_visible=True
    )

    fig.update_layout(
        showlegend=False,
        height=500,
        margin=dict(l=0, r=20, t=20, b=0),
        plot_bgcolor='white',
        paper_bgcolor='#e1efff'
    )
    return fig

# ==========================
# RSI CHART
# ==========================
def RSI(dataframe, num_period):
    dataframe['RSI'] = pta.rsi(dataframe['Close'])
    dataframe = filter_data(dataframe, num_period)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['RSI'],
        name='RSI', line=dict(width=2, color='orange')
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=[70] * len(dataframe),
        name='Overbought', line=dict(width=2, color='red', dash='dash')
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=[30] * len(dataframe),
        name='Oversold', fill='tonexty', line=dict(width=2, color='#79da84', dash='dash')
    ))

    fig.update_xaxes(
        tickformat="%Y-%m-%d", tickangle=45
    )

    fig.update_layout(
        yaxis_range=[0, 100],
        height=200,
        plot_bgcolor='white',
        paper_bgcolor='#e1efff',
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(orientation="h", yanchor="top", y=1.02, xanchor="right", x=1)
    )
    return fig

# ==========================
# MOVING AVERAGE CHART
# ==========================
def Moving_average(dataframe, num_period):
    dataframe['SMA_50'] = pta.sma(dataframe['Close'], 50)
    dataframe = filter_data(dataframe, num_period)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['Open'],
        mode='lines', name='Open', line=dict(width=2, color='#5ab7ff')
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['Close'],
        mode='lines', name='Close', line=dict(width=2, color='black')
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['SMA_50'],
        mode='lines', name='SMA 50', line=dict(width=2, color='green')
    ))

    fig.update_xaxes(
        rangeslider_visible=True,
        tickformat="%Y-%m-%d", tickangle=45
    )

    fig.update_layout(
        height=500,
        margin=dict(l=0, r=20, t=20, b=0),
        plot_bgcolor='white',
        paper_bgcolor='#e1efff',
        legend=dict(yanchor="top", xanchor="right")
    )
    return fig

# ==========================
# MACD CHART
# ==========================
def MACD(dataframe, num_period):
    macd_df = pta.macd(dataframe['Close'])
    dataframe['MACD'] = macd_df.iloc[:, 0]
    dataframe['MACD_Signal'] = macd_df.iloc[:, 1]
    dataframe['MACD_Hist'] = macd_df.iloc[:, 2]

    dataframe = filter_data(dataframe, num_period)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['MACD'],
        name='MACD', line=dict(width=2, color='orange')
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['MACD_Signal'],
        name='Signal', line=dict(width=2, color='red', dash='dash')
    ))

    fig.add_trace(go.Bar(
        x=dataframe['Date'], y=dataframe['MACD_Hist'],
        name='Histogram',
        marker_color=['red' if val < 0 else 'green' for val in dataframe['MACD_Hist']]
    ))

    fig.update_xaxes(
        tickformat="%Y-%m-%d", tickangle=45
    )

    fig.update_layout(
        height=200,
        plot_bgcolor='white',
        paper_bgcolor='#e1efff',
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(orientation="h", yanchor="top", y=1.02, xanchor="right", x=1)
    )
    return fig

# ==========================
# MOVING AVERAGE FORECAST
# ==========================
def Moving_average_forecast(forecast):
    forecast.index = pd.to_datetime(forecast.index)
    forecast['Date'] = forecast.index.date

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=forecast['Date'][:-30],
        y=forecast['Close'].iloc[:-30],
        mode='lines', name='Close Price', line=dict(width=2, color='black')
    ))

    fig.add_trace(go.Scatter(
        x=forecast['Date'][-31:],
        y=forecast['Close'].iloc[-31:],
        mode='lines', name='Future Close Price', line=dict(width=2, color='red')
    ))

    fig.update_xaxes(
        rangeslider_visible=True,
        tickformat="%Y-%m-%d", tickangle=45
    )

    fig.update_layout(
        height=500,
        margin=dict(l=0, r=20, t=20, b=20),
        plot_bgcolor='white',
        paper_bgcolor='#e1efff',
        legend=dict(yanchor="top", xanchor="right")
    )
    return fig
