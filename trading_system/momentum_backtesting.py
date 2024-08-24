from trading_system.backtesting import Backtesting
from trading_system.momentum_strategy import MomentumStrategy
import matplotlib.pyplot as plt
import streamlit as st

class MomentumBacktesting(Backtesting):
    def __init__(self, strategy, initial_capital):
        super().__init__(strategy, initial_capital)
        self.strategy = strategy
        self.initial_capital = initial_capital


    def run_backtest(self):
        signals = self.strategy.generate_signals()
        # print(signals)

        for index, row in signals.iterrows():
            if row['Signal'] == 1 and self.position == 0:
                # Buy signal
                self.position = self.cash / row['Close']
                self.cash = 0
                buy_price = row['Close']
                self.positions.append((index, 'Buy', buy_price))
            elif row['Signal'] == -1 and self.position > 0:
                # Sell signal
                self.cash = self.position * row['Close']
                self.position = 0
                sell_price = row['Close']
                self.positions.append((index, 'Sell', sell_price))
            numeric_value = self.cash + self.position * row['Close']
            # debugging~
            # st.write(f"Type of numeric_value: {type(numeric_value)}")
            self.portfolio_value.append(int(numeric_value))

    def performative_metrics(self):
        # self.data['Portfolio_Value'] = self.portfolio_value
        final_value = self.portfolio_value[-1]
        total_return = round((final_value - self.initial_capital) / self.initial_capital * 100)
        self.final_value = final_value
        self.total_return = total_return
        print(f"Initial Cash: {self.initial_capital}")
        print(f"Final Portfolio Value: {final_value}")
        print(f"Total Return: {(final_value - self.initial_capital) / self.initial_capital * 100:.2f}%")

    def plot_indicators(self):
        data = self.strategy.data
        st.line_chart(self.strategy.data[['Close', '50_SMA', '200_SMA']])
        st.line_chart(self.strategy.data[['RSI']])
        # Plot the close price along with the indicators
        plt.figure(figsize=(14, 7))

        # Plot the close price
        plt.plot(data['Close'], label='Close Price', color='blue')

        # Plot the 50-SMA
        plt.plot(data['50_SMA'], label='50-SMA', color='orange')

        # Plot the 200-SMA
        plt.plot(data['200_SMA'], label='200-SMA', color='green')

        # Plot the RSI (you might want to plot this on a separate subplot)
        plt.figure(figsize=(14, 7))
        plt.plot(data['RSI'], label='RSI', color='red')
        plt.axhline(y=70, color='gray', linestyle='--')  # Overbought line
        plt.axhline(y=30, color='gray', linestyle='--')  # Oversold line

        plt.title("Stock Indicators")
        plt.legend()
        plt.show()

        # Display the plot in Streamlit
        # st.pyplot(plt)
    def plot_results(self):
        pass

# strategy = MomentumStrategy("AAPL", '2010-01-01', '2020-01-01')
# strategy.download_data("AAPL", '2010-01-01', '2020-01-01')
# strategy.calculate_indicators()
# strategy.generate_signals()
# aapl_momentum_backtest = MomentumBacktesting(strategy=strategy, initial_capital=10000)
# aapl_momentum_backtest.run_backtest()
# aapl_momentum_backtest.performative_metrics()