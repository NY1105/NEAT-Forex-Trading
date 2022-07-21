from numpy import rec
import plotly.graph_objects as go
import pandas as pd

SYMBOL = 'EURUSD'
MODE = 'test'


def visualise(mode=MODE, symbol=SYMBOL):
    df = pd.read_csv(f'data/csv/{symbol}/_{symbol}_{mode}.csv')
    df = df.set_index(pd.DatetimeIndex(df['Datetime'].values))
    df.drop(df[df.Volume == 0].index, inplace=True)

    record = pd.read_csv(f'result/{symbol}_{mode}_result.csv')
    buy = record.drop(record[record.Type != 'Buy'].index)
    record = pd.read_csv(f'result/{symbol}_{mode}_result.csv')
    sell = record.drop(record[record.Type != 'Sell'].index)
    record = pd.read_csv(f'result/{symbol}_{mode}_result.csv')
    close = record.drop(record[record.Type != 'Close'].index)
    figure = go.Figure(
        data=[
            go.Candlestick(
                name='Candlestick',
                x=df.index,
                low=df['Low'],
                high=df['High'],
                close=df['Close'],
                open=df['Open'],
                increasing_line_color='green',
                decreasing_line_color='red'
            ),
            go.Scatter(
                mode='markers',
                name='Buy',
                marker=dict(color='Blue', size=11, line=dict(width=2, color='DarkSlateGrey')),
                line=dict(width=0),
                y=buy['Price'],
                x=buy['Index']
            ),
            go.Scatter(
                mode='markers',
                name='Sell',
                marker=dict(color='Orange', size=11, line=dict(width=2, color='DarkSlateGrey')),
                line=dict(width=0),
                y=sell['Price'],
                x=sell['Index']
            ),
            go.Scatter(
                mode='markers',
                name='Close',
                marker=dict(color='Lime', size=11, line=dict(width=2, color='DarkSlateGrey')),
                line=dict(width=0),
                y=close['Price'],
                x=close['Index']
            ),
        ]
    )
    figure.update_layout(xaxis_rangeslider_visible=False)
    figure.show()
