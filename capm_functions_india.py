import plotly.express as px
import numpy as np
import pandas as pd

def interactive_plot(df):
    fig = px.line()
    for col in df.columns[1:]:
        fig.add_scatter(x=df['Date'], y=df[col], name=col)
    
    fig.update_layout(
        width=450,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    return fig

def normalize(df):
    df_norm = df.copy()
    for col in df_norm.columns[1:]:
        df_norm[col] = df_norm[col] / df_norm[col].iloc[0]
    return df_norm

def daily_return(df):
    df_return = df.copy()
    for col in df.columns[1:]:
        df_return[col] = df[col].pct_change().fillna(0) * 100
    return df_return

def calculate_beta(daily_returns_df, stock, market='Nifty50'):
    beta, alpha = np.polyfit(daily_returns_df[market], daily_returns_df[stock], 1)
    return beta, alpha
