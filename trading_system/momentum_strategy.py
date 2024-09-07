import numpy as np
import yfinance as yf
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator
from trading_system.strategy import Strategy
from requests.exceptions import RequestException
import streamlit as st

class MomentumStrategy(Strategy):

    def download_data(self, ticker, start_date, end_date):
        # ticker = 'AAPL'  # Example ticker
        # start_date = '2010-01-01'
        # end_date = '2020-01-01'
        try:
            self.data = yf.download(ticker, start=start_date, end=end_date)
            print("Data downloaded successfully.")
        except RequestException as e:
            st.write(f"Network-related error: {e}")
            self.data = None
        except Exception as e:
            st.write(f"An error occurred: {e}")
            self.data = None
        print("working")
        # print(self.data)

    def calculate_indicators(self):
        self.data['50_SMA'] = SMAIndicator(self.data['Close'], window=50).sma_indicator()
        self.data['200_SMA'] = SMAIndicator(self.data['Close'], window=200).sma_indicator()
        self.data['RSI'] = RSIIndicator(self.data['Close'], window=14).rsi()

        # print(self.data['RSI'])
        print("working")

    def generate_signals(self):
        # Default to no signal
        self.data['Signal'] = 0

        # Calculate the conditions for crossovers
        condition1 = (self.data['50_SMA'].shift(1) <= self.data['200_SMA'].shift(1)) & (
                self.data['50_SMA'] > self.data['200_SMA'])  # Cross up
        condition2 = (self.data['50_SMA'].shift(1) >= self.data['200_SMA'].shift(1)) & (
                self.data['50_SMA'] < self.data['200_SMA'])  # Cross down

        # Generate Buy Signal on upward crossover and additional RSI condition
        self.data['Signal'] = np.where(condition1 & (self.data['RSI'] > 50) & (self.data['RSI'] < 70), 1,
                                       self.data['Signal'])

        # Generate Sell Signal on downward crossover and additional RSI condition
        self.data['Signal'] = np.where(condition2 & (self.data['RSI'] < 50) & (self.data['RSI'] > 30), -1,
                                       self.data['Signal'])

        print("working")
        return self.data
        # print(self.data['Signal'])


# aapl_momentum = MomentumStrategy("AAPL", '2010-01-01', '2020-01-01')
# aapl_momentum.download_data("AAPL", '2010-01-01', '2020-01-01')
# aapl_momentum.calculate_indicators()
# aapl_momentum.generate_signals()