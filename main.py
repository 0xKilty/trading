import yfinance
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#Get historical data
tsla = yfinance.Ticker("TSLA")
hist = tsla.history(period="2y")

#Init plot
plot = make_subplots(specs=[[{"secondary_y": True}]])

#Top label
plot.update_layout(title={'text':'TSLA', 'x':0.5})

#Candlestick
plot.add_trace(go.Candlestick(x=hist.index,
                              open=hist['Open'],
                              high=hist['High'],
                              low=hist['Low'],
                              close=hist['Close'],
                              name='Price'
                             ))

MA20 = hist['Close'].rolling(window=20).mean()
MA10 = hist['Close'].rolling(window=10).mean()


buy = []
sell = []
for i in range(len(MA20)-1):
    if MA10[i] > MA20[i] and MA10[i+1] <= MA20[i+1]:
        sell.append(i)
    elif MA10[i] < MA20[i] and MA10[i+1] >= MA20[i+1]:
        buy.append(i)

plot.add_trace(go.Scatter(x=hist.index, y=MA20, marker_color='blue', name='20 Day MA'))
plot.add_trace(go.Scatter(x=hist.index, y=MA10, marker_color='orange', name='10 Day MA'))
plot.add_trace(go.Scatter(x=hist.iloc[buy].index, 
                          y=hist.iloc[buy]['Close'], 
                          mode='markers',
                          marker_symbol="diamond-dot",
                          marker_size=13,
                          marker_color='green', 
                          marker_line_color='black',
                          marker_line_width=2,
                          hovertemplate="Buy $%{y}",
                          name='Buy'))

plot.add_trace(go.Scatter(x=hist.iloc[sell].index, 
                          y=hist.iloc[sell]['Close'], 
                          mode='markers',
                          marker_symbol="diamond-dot",
                          marker_size=13,
                          marker_color='red', 
                          marker_line_color='black',
                          marker_line_width=2,
                          hovertemplate="Sell $%{y}",
                          name='Sell'))

def percent_difference(a, b):
    return (b - a) / a

actions = pd.concat([hist.iloc[buy]['Close'], hist.iloc[sell]['Close']])
actions = actions.sort_index()
total_change = 0
current_value = 100
for i in range(len(actions)-1):
    current_value *= percent_difference(actions[i], actions[i+1]) + 1
    print(current_value)
    total_change += int(((actions[i+1] - actions[i])) / actions[i])

print(percent_difference(100, current_value))

#Volume
#plot.add_trace(go.Bar(x=hist.index, y=hist['Volume'], name='Volume'), secondary_y=True)
#plot.update_yaxes(range=[0,1000000000], secondary_y=True)

plot.update_yaxes(visible=False, secondary_y=True) #hide the volume units
plot.update_layout(xaxis_rangeslider_visible=False)  #hide range slider
plot.update_xaxes(rangebreaks = [dict(bounds=['sat','mon']), # hide weekends
                                 #dict(bounds=[16, 9.5], pattern='hour'), # for hourly chart, hide non-trading hours (24hr format)
                                 dict(values=["2021-12-25","2022-01-01"]) #hide Xmas and New Year
                                ])

plot.show()
