from matplotlib.pyplot import title
from numpy import tile
import plotly.graph_objects as go
import pandas as pd
from indicators import Indicators

SYMBOL = 'EURUSD'
MODE = 'test'


def visualise(cash, mode=MODE, symbol=SYMBOL):
    df = Indicators(symbol, mode).get_df()

    record = pd.read_csv(f'result/{symbol}_{mode}_result.csv')
    open_buy_sell = record.drop(record[record.Type == 'Close'].index)
    record = pd.read_csv(f'result/{symbol}_{mode}_result.csv')
    close = record.drop(record[record.Type != 'Close'].index)

    open_and_close = []
    for i in range(len(close)):
        color = 'Orange'
        if open_buy_sell['Type'].iloc[i] == 'Buy':
            color = 'Blue'
        open_and_close.append(
            go.Scatter(
                name=open_buy_sell['Type'].iloc[i],
                marker=dict(color=color, size=9, line=dict(width=2, color='DarkSlateGrey')),
                y=[open_buy_sell['Price'].iloc[i], close['Price'].iloc[i]],
                x=[open_buy_sell['Index'].iloc[i], close['Index'].iloc[i]],
                text=f'Profit: {close["Profit"].iloc[i]}',
                hoverinfo='text',
                showlegend=False
            ),
        )
    data = [
        go.Candlestick(
            name='Candlestick',
            x=df['Datetime'],
            low=df['Low'],
            high=df['High'],
            close=df['Close'],
            open=df['Open'],
            increasing_line_color='green',
            decreasing_line_color='red'
        ),
    ]
    data += open_and_close
    figure = go.Figure(data)
    figure.update_layout(xaxis_rangeslider_visible=False,xaxis_title="Timeframe", yaxis_title="Price", legend_title=f"Balance: {cash}; Opens: {len(open_and_close)}",)
    figure.show()
