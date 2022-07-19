from numpy import rec
import plotly.graph_objects as go
import pandas as pd

SYMBOL = 'EURUSD'
MODE = 'test'

df = pd.read_csv(f'data/csv/_{SYMBOL}_{MODE}.csv')
df = df.set_index(pd.DatetimeIndex(df['Unnamed: 0'].values))
df.drop(df[df.Volume == 0].index, inplace=True)

record = pd.read_csv(f'result/{SYMBOL}_result.csv')

figure = go.Figure(
    data=[
        go.Candlestick(
            x=df.index,
            low=df['Low'],
            high=df['High'],
            close=df['Close'],
            open=df['Open'],
            increasing_line_color='green',
            decreasing_line_color='red'
        ),
        go.Scatter(
            y=record['Price'],
            x=record['Index']
        )
    ]
)


figure.show()
