import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator
import numpy as np
import streamlit as st


class MomentumStrategy:
    def __init__(self, ticker, start_date, end_date, initial_cash=10000):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.initial_cash = initial_cash
        self.data = None
        self.positions = []
        self.portfolio_value = []

    def download_data(self):
        self.data = yf.download(self.ticker, start=self.start_date, end=self.end_date)

    def calculate_indicators(self):
        self.data['50_SMA'] = SMAIndicator(self.data['Close'], window=50).sma_indicator()
        self.data['200_SMA'] = SMAIndicator(self.data['Close'], window=200).sma_indicator()
        self.data['RSI'] = RSIIndicator(self.data['Close'], window=14).rsi()

    def generate_signals(self):
        self.data['Signal'] = 0  # Default to no signal
        self.data['Signal'] = np.where(
            (self.data['50_SMA'] > self.data['200_SMA']) &
            (self.data['RSI'] > 50) &
            (self.data['RSI'] < 70),
            1,
            self.data['Signal']
        )
        self.data['Signal'] = np.where(
            (self.data['50_SMA'] < self.data['200_SMA']) &
            (self.data['RSI'] < 50) &
            (self.data['RSI'] > 30),
            -1,
            self.data['Signal']
        )
        self.data['Signal'] = self.data['Signal'].replace(to_replace=0, method='ffill')

    def backtest_strategy(self):
        cash = self.initial_cash
        position = 0

        for index, row in self.data.iterrows():
            if row['Signal'] == 1 and position == 0:
                # Buy signal
                position = cash / row['Close']
                cash = 0
                buy_price = row['Close']
                self.positions.append((index, 'Buy', buy_price))
            elif row['Signal'] == -1 and position > 0:
                # Sell signal
                cash = position * row['Close']
                position = 0
                sell_price = row['Close']
                self.positions.append((index, 'Sell', sell_price))
            self.portfolio_value.append(cash + position * row['Close'])

        self.data['Portfolio_Value'] = self.portfolio_value
        final_value = self.portfolio_value[-1]
        return final_value

    def plot_results(self):
        plt.figure(figsize=(14, 7))
        plt.plot(self.data.index, self.data['Portfolio_Value'], label='Portfolio Value')
        plt.plot(self.data.index, self.data['Close'], label='Close Price', alpha=0.5)
        for position in self.positions:
            if position[1] == 'Buy':
                plt.plot(position[0], position[2], '^', markersize=10, color='g', label='Buy Signal')
            elif position[1] == 'Sell':
                plt.plot(position[0], position[2], 'v', markersize=10, color='r', label='Sell Signal')
        plt.title('Momentum Trading Strategy Backtest')
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.legend()
        st.pyplot(plt)  # Use Streamlit's pyplot function to render the plot in the app

    def run(self):
        self.download_data()
        self.calculate_indicators()
        self.generate_signals()
        final_value = self.backtest_strategy()
        return final_value


# Integration into Streamlit app
def main():
    st.title("Momentum Strategy Backtester")

    ticker = st.text_input("Enter Ticker", "AAPL")
    start_date = st.date_input("Start Date", value=pd.to_datetime("2010-01-01"))
    end_date = st.date_input("End Date", value=pd.to_datetime("2020-01-01"))
    initial_cash = st.number_input("Initial Cash", value=10000)

    if st.button("Run Backtest"):
        strategy = MomentumStrategy(ticker, start_date, end_date, initial_cash)
        final_value = strategy.run()
        st.write(f"Final Portfolio Value: ${final_value:.2f}")
        st.write(f"Total Return: {(final_value - initial_cash) / initial_cash * 100:.2f}%")
        strategy.plot_results()


if __name__ == "__main__":
    main()
