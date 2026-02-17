import streamlit as st

import polars as pl
import pandas as pd

import plotly.graph_objects as go
import plotly.express as px

from src.utils import load_data, init_session_states
from src.charts import choropleth_top_10_by_state
import src.widgets as widgets
import src.pipes as pipes



# load sessions and data
init_session_states()
state_data = load_data('data/state_data.parquet')

if st.session_state.sex == 'F':
    sex_title = 'Female'
else:
    sex_title = 'Male'


# Define Header
if st.session_state.year_range[0] == st.session_state.year_range[1]:
    header = f'Top {sex_title} Names by State - {st.session_state.year_range[0]}'
else:
    header = f'Top {sex_title} Names by State - {st.session_state.year_range[0]} to {st.session_state.year_range[1]}'
st.header(header)

with st.popover('Filters'):
    widgets.year_range_slider()
    widgets.sex_radio()



###############
# Map of US
###############

temp_df = (
    state_data
    .pipe(pipes.filter_year, st.session_state['year_range'])
    .pipe(pipes.filter_sex, st.session_state['sex'])
    .collect(engine='streaming')
)

st.plotly_chart(choropleth_top_10_by_state())


