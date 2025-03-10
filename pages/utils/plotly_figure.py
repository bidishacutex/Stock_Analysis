import plotly.graph_objects as go
import pandas_ta as pta
import dateutil
import datetime

def plotly_table(dataframe):
    headerColor = 'grey'
    rowEvenColor = '#f8fafd'
    rowOddColor = '#e1efff' 

    # Generate alternating colors for the rows
    fill_colors = [
        rowOddColor if i % 2 == 0 else rowEvenColor
        for i in range(len(dataframe))
    ]

    fig = go.Figure(data=[go.Table(
        header = dict(
            values = ["<b><b>"]+["<b>" + str(i)[:10]+"<b>" for i in dataframe.columns],
            line_color = '#0078ff',
            fill_color = '#0078ff',
            align='center',
            font=dict(color='white', size=15),
            height=35
        ),
        cells=dict(
            values=[["<b>"+str(i)+"<b>" for i in dataframe.index]]+[dataframe[i] for i in dataframe.columns],
            line_color='white',
            fill_color = [fill_colors] * len(dataframe.columns),
            align='left',
            font=dict(color='black', size=15)
        )
    )])

    fig.update_layout(height=400, margin=dict(l=0, r=0, t=0, b=0))
    return fig