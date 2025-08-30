import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="Reviews de hospedagens no Rio de Janeiro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Reviews de hospedagens no Rio de Janeiro")
