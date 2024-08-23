import numpy as np
import pandas as pd
import streamlit as st
import datetime
import matplotlib.pyplot as plt
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator
from test import MomentumStrategy

st.set_page_config(layout='wide')
st.title("BlackElm Backtesting Enviroment")
col1,col2 = st.columns([2,3])
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
    user_initial_capital = st.text_input("Enter initial capital", key='initial_capital')
    if user_initial_capital:
        st.write(f"Initial capital: {user_initial_capital}")

    st.subheader("Enter the backtesting period")
    user_start_date = st.date_input("Start date", value=pd.to_datetime("2010-01-01"))
    user_end_date = st.date_input("End date", value=pd.to_datetime("2010-01-01"))
    st.write("START DATE:", user_start_date)
    st.write("END DATE:", user_end_date)

#checking if info is stored properly
    st.write(user_ticker)
    st.write(user_initial_capital)



with col2:
    tile2 = col2.container()
    tile2.title("Strategy Results")
    ticker = user_ticker
    initial_capital = user_initial_capital
    start_date = user_start_date
    end_date = user_end_date

    if st.button("Run Backtest"):
        strategy = MomentumStrategy(ticker, start_date, end_date, initial_capital)
        final_value = strategy.run()
        st.write(f"Final Portfolio Value: ${final_value:.2f}")
        st.write(f"Total Return: {(final_value - initial_capital) / initial_capital * 100:.2f}%")
        strategy.plot_results()


    # tab1, tab2, tab3 = tile2.tabs(["users", "new", "edit"])
    #
    # with tab1:
    #     df = pd.DataFrame(np.random.randn(10, 5), columns=("col %d" % i for i in range(5)))
    #
    #     st.dataframe(df, use_container_width=True)
    #
    # with tab2:
    #     st.header("A dog")
    #     st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
    #
    # with tab3:
    #     st.header("An owl")
    #     st.image("https://static.streamlit.io/examples/owl.jpg", width=200)