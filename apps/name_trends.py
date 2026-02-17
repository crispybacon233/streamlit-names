import streamlit as st
import polars as pl

import plotly.express as px

import src.widgets as widgets
import src.pipes as pipes
from src.utils import load_national_data, load_state_data


# Load data
national_data = load_national_data()
state_data = load_state_data()


with st.popover('Filters'):
    widgets.year_range_slider()
    widgets.name_select()


temp_df = (
    state_data
    .pipe(pipes.name_filter, st.session_state['name_filter'])
    .group_by('name', 'year')
    .agg(pl.col('count').sum())
    .sort(by=['name', 'year'])
)

line_chart = px.line(
    data_frame=temp_df,
    x='year',
    y='count',
    color='name'
)

st.plotly_chart(line_chart, width='content')