import streamlit as st

from pages import momentum_page1
from pages import momentum_page2

pages = {
    "Momentum Page 1": momentum_page1,
    "Momentum Page 2": momentum_page2
}

st.set_page_config(layout='wide')
st.title("BlackElm Backtesting Enviroment")
