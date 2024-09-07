from trading_system.backtesting import Backtesting
from trading_system.momentum_strategy import MomentumStrategy
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

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

    def scoring(self):

        def get_next_available_date(data, end_date):
            while end_date not in data.index:
                end_date += pd.Timedelta(days=1)  # Increment the end_date until a valid trading day is found
            return end_date

        data = self.strategy.generate_signals()
        results = []
        time_frames = [7, 30, 90]


        for i, row in data.iterrows():
            if row['Signal'] != 0:  # Signal exists
                signal_date = i
                signal_price = row['Close']
                signal_type = 'Buy' if row['Signal'] == 1 else 'Sell'

                for days in time_frames:
                    # Calculate the date range to look ahead
                    end_date = signal_date + pd.Timedelta(days=days)

                    if end_date not in data.index:
                        end_date = get_next_available_date(data, end_date)

                    if end_date in data.index:
                        # Calculate the price change over the time frame
                        future_price = data.loc[end_date, 'Close']
                        price_change = future_price - signal_price
                        mean_price = data.loc[signal_date:end_date, 'Close'].mean()
                        std_dev = data.loc[signal_date:end_date, 'Close'].std()

                        # Calculate the number of standard deviations the price moved
                        if std_dev != 0:
                            std_devs_moved = (future_price - mean_price) / std_dev
                        else:
                            std_devs_moved = 0

                        # Scoring based on the type of signal
                        if signal_type == 'Buy':
                            if std_devs_moved <= 0:
                                score = 0
                            elif std_devs_moved >=2:
                                score = 10
                            else:
                                score = (std_devs_moved/2) * 10
                        else:  # Sell
                            if std_devs_moved >= 0:
                                score = 0
                            elif std_devs_moved <= -2:
                                score = 10
                            else:
                                score = (-std_devs_moved / 2) * 10

                        # Append results
                        results.append({
                            'Signal Date': signal_date,
                            'Signal Type': signal_type,
                            'Time Frame': days,
                            'Future Price': future_price,
                            'Price Change': price_change,
                            'Std Devs Moved': std_devs_moved,
                            'Score': score
                        })

        return pd.DataFrame(results)

# strategy = MomentumStrategy("AAPL", '2010-01-01', '2020-01-01')
# strategy.download_data("AAPL", '2010-01-01', '2020-01-01')
# strategy.calculate_indicators()
# strategy.generate_signals()
# aapl_momentum_backtest = MomentumBacktesting(strategy=strategy, initial_capital=10000)
# aapl_momentum_backtest.run_backtest()
# aapl_momentum_backtest.performative_metrics()