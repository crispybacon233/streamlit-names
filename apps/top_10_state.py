import streamlit as st

import polars as pl
import pandas as pd

import plotly.graph_objects as go
import plotly.express as px

from src.utils import load_state_names
import src.widgets as widgets
import src.pipes as pipes


state_data = load_state_names()


st.header('Top 10 Names by State')

widgets.year_range_slider()



###############
# Map of US
###############

temp_df = (
    state_data
    .pipe(pipes.filter_year, st.session_state['year_range'])
)

st.dataframe(temp_df.head(500))
st.write(st.session_state['year_range'])


