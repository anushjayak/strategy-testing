import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator
import numpy as np

# Download historical data for a given stock
ticker = 'AAPL'  # Example ticker
start_date = '2010-01-01'
end_date = '2020-01-01'
data = yf.download(ticker, start=start_date, end=end_date)

# Calculate indicators
data['50_SMA'] = SMAIndicator(data['Close'], window=50).sma_indicator()
data['200_SMA'] = SMAIndicator(data['Close'], window=200).sma_indicator()
data['RSI'] = RSIIndicator(data['Close'], window=14).rsi()

# Define buy and sell signals
data['Signal'] = 0  # Default to no signal
data['Signal'] = np.where((data['50_SMA'] > data['200_SMA']) & (data['RSI'] > 50) & (data['RSI'] < 70), 1, data['Signal'])
data['Signal'] = np.where((data['50_SMA'] < data['200_SMA']) & (data['RSI'] < 50) & (data['RSI'] > 30), -1, data['Signal'])

# Forward fill the signals
data['Signal'] = data['Signal'].replace(to_replace=0, method='ffill')

# Backtest strategy
initial_cash = 10000
cash = initial_cash
position = 0
positions = []
portfolio_value = []

for index, row in data.iterrows():
    if row['Signal'] == 1 and position == 0:
        # Buy signal
        position = cash / row['Close']
        cash = 0
        buy_price = row['Close']
        positions.append((index, 'Buy', buy_price))
    elif row['Signal'] == -1 and position > 0:
        # Sell signal
        cash = position * row['Close']
        position = 0
        sell_price = row['Close']
        positions.append((index, 'Sell', sell_price))
    portfolio_value.append(cash + position * row['Close'])

# Results
data['Portfolio_Value'] = portfolio_value
final_value = portfolio_value[-1]

# Print results
print(f"Initial Cash: {initial_cash}")
print(f"Final Portfolio Value: {final_value}")
print(f"Total Return: {(final_value - initial_cash) / initial_cash * 100:.2f}%")

# Plot results
plt.figure(figsize=(14, 7))
plt.plot(data.index, data['Portfolio_Value'], label='Portfolio Value')
plt.plot(data.index, data['Close'], label='Close Price', alpha=0.5)
for position in positions:
    if position[1] == 'Buy':
        plt.plot(position[0], position[2], '^', markersize=10, color='g', label='Buy Signal')
    elif position[1] == 'Sell':
        plt.plot(position[0], position[2], 'v', markersize=10, color='r', label='Sell Signal')
plt.title('Momentum Trading Strategy Backtest')
plt.xlabel('Date')
plt.ylabel('Value')
plt.legend()
plt.show()
