import pandas_ta as ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

def macd(df):
   #MACD Calculation 
    macddf = df.ta.macd(close='v',fast=12, slow=26, signal=9, append=True)
    macdf=macddf['MACD_12_26_9'] # fast signal
    macds=macddf['MACDs_12_26_9'] #slow signal
    macdh=macddf['MACDh_12_26_9'] #histogram
    #RSI Calculation

    fastlist = list(macdf)
    slowlist = list(macds)

    macd_bull = fastlist[-2]<0 and fastlist[-1]>0 #macd uptrend
    macd_bear = fastlist[-2]>0 and fastlist[-1]<0 #macd downtrend
    return macd_bull, macd_bear 
    
def boll(df):
    value = df['v']
    sma = value.rolling(20).mean() # calculate middle band
    std = value.rolling(20).std()
    bollinger_up = sma + std * 2 # Calculate top band
    bollinger_down = sma - std * 2 # Calculate bottom band

    boll_bear = value[-1]>bollinger_up[-1] # value exceeds boll top band, bearish
    boll_bull = value[-1]<bollinger_down[-1] #value drop below low band, bullish
    return boll_bull, boll_bear

def rsi(df):
    value=list(df['v'])
    rsidf = ta.rsi(value, length=14)
    rsilist = list(rsidf)
    
    rsi_bear = rsilist[-1] >80 #rsi overbought, bearish
    rsi_bull = rsilist[-1] <20 # oversold, bullish
    return rsi_bear, rsi_bull

def trend_alert(macd_bull, macd_bear,boll_bull, boll_bear,rsi_bear, rsi_bull):
    




















def graph():
    #Graph
    if graph:
        fig = make_subplots(rows=3, cols=1)
        fig.append_trace(
            go.Scatter(
                x=datelist,
                y=rsidf,
                line=dict(color='green', width=1),
                name='RSI',
                # showlegend=False,
                legendgroup='1',
            ), row=3, col=1
        )

        fig.append_trace(
            go.Scatter(
                x=datelist,
                y=df['v'],
                line=dict(color='#ff9900', width=1),
                name='Min1 BTC Address',
                # showlegend=False,
                legendgroup='1',
            ), row=1, col=1
        )
        #fast signal
        fig.append_trace(
            go.Scatter(
                x=datelist,
                y=macdf,
                line=dict(color='#ff9900', width=2),
                name='macd fast',
                # showlegend=False,
                legendgroup='2',
            ), row=2, col=1
        )
        # Slow signal (%d)
        fig.append_trace(
            go.Scatter(
                x=datelist,
                y=macds,
                line=dict(color='#000000', width=2),
                # showlegend=False,
                legendgroup='2',
                name='macd slow signal'
            ), row=2, col=1
        )   
        # Colorize the histogram values
        colors = np.where(macdh < 0, '#000', '#ff9900')
        # Plot the histogram
        fig.append_trace(
            go.Bar(
                x=datelist,
                y=macdh,
                name='histogram',
                marker_color=colors,
            ), row=2, col=1
        )
        # Make it pretty
        layout = go.Layout(
            plot_bgcolor='#efefef',
            # Font Families
            font_family='Monospace',
            font_color='#000000',
            font_size=20,
            xaxis=dict(
                rangeslider=dict(
                    visible=False
                )
            )
        )
        # Update options and show plot
        fig.update_layout(layout)
        fig.show()
