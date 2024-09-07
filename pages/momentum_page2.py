import numpy as np
import pandas as pd
import streamlit as st
import datetime
import matplotlib.pyplot as plt
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator
from trading_system.momentum_strategy import MomentumStrategy
from trading_system.momentum_backtesting import MomentumBacktesting

st.set_page_config(layout="wide")
st.title("Momentum Strategy Backtester")
col1, col2, col3 = st.columns([1, 3, 1])
ticker = ""
initial_capital = 0

with col1:
    tile1 = col1.container()
    tile1.header("Backtesting parameters:")

    st.subheader("Enter the ticker below")
    user_ticker = st.text_input("Enter ticker", key='ticker')
    if user_ticker:
        st.write(f"Following ticker has been selected: {user_ticker}")
    st.subheader("Enter the initial capital below")
    user_initial_capital = st.number_input("Enter initial capital", key='initial_capital', min_value=0, step=1,
                                           format="%d")
    if user_initial_capital:
        st.write(f"Initial capital: {user_initial_capital}")
    final_value = 0
    total_return = 0

    st.subheader("Enter the backtesting period")
    user_start_date = st.date_input("Start date", value=pd.to_datetime("2010-01-01"))
    user_end_date = st.date_input("End date", value=pd.to_datetime("2018-01-01"))
    st.write("START DATE:", user_start_date)
    st.write("END DATE:", user_end_date)

# checking if info is stored properly
# st.write(user_ticker)
# st.write(user_initial_capital)

with col2:
    tile2 = col2.container()
    tile2.header("Graphs")

    if st.button("Run Backtest"):
        strategy = MomentumStrategy(user_ticker, user_start_date, user_end_date)
        strategy.download_data(user_ticker, user_start_date, user_end_date)
        strategy.calculate_indicators()
        strategy.generate_signals()
        strategy_backtest = MomentumBacktesting(strategy=strategy, initial_capital=int(user_initial_capital))
        strategy_backtest.run_backtest()
        strategy_backtest.performative_metrics()
        strategy_backtest.plot_indicators()
        final_value = strategy_backtest.final_value
        total_return = strategy_backtest.total_return
        # st.subheader(f"Initial Cash: {user_initial_capital}$")
        # st.subheader(f"Final Value: {strategy_backtest.final_value}$")
        # st.subheader(f"Total Return: {strategy_backtest.total_return}%")
        # st.write(f"Final value: {strategy_backtest.final_value}")

with col3:
    tile3 = col3.container()
    tile3.header("Performative Metrics")
    st.subheader(f"Initial Cash: {user_initial_capital}$")
    st.subheader(f"Final Value: {final_value}$")
    st.subheader(f"Total Return: {total_return}%")


# strategy = MomentumStrategy("AAPL", '2010-01-01', '2020-01-01')
# strategy.download_data("AAPL", '2010-01-01', '2020-01-01')
# strategy.calculate_indicators()
# strategy.generate_signals()
# aapl_momentum_backtest = MomentumBacktesting(strategy=strategy, initial_capital=10000)
# aapl_momentum_backtest.run_backtest()
# aapl_momentum_backtest.performative_metrics()