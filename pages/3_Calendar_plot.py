import streamlit as st
import pandas as pd
from plotly_calplot import calplot

st.set_page_config(
    page_title='Calendar Plot',
    layout="wide",
    page_icon="📅",
    initial_sidebar_state="expanded"
)

dummy_df = pd.read_csv("data/messages_data.csv")

fig = calplot(
    dummy_df,
    x="ds",
    y="value",
    title = "Work Group Messages",
    showscale=True, 
    years_title = True
)

st.plotly_chart(fig, use_container_width=True)