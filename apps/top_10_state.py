import streamlit as st

import polars as pl
import pandas as pd

import plotly.graph_objects as go
import plotly.express as px

from src.utils import load_state_names
from src.widgets import year_range_slider


state_data = load_state_names()


st.header('Top 10 Names by State')

year_range_slider()



###############
# Map of US
###############
year_range = st.session_state['year_range']

temp_df = (
    state_data
    .filter(pl.col('year').is_between(year_range[0], year_range[1]))
)

st.dataframe(temp_df.head(500))
st.write(st.session_state['year_range'])


