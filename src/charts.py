import streamlit as st
import polars as pl
import plotly.express as px


import src.pipes as pipes
from src.utils import load_data


# Load data
national_data = load_data('data/national_data.parquet')
state_data = load_data('data/state_data.parquet')


def line_chart_name_counts():
    temp_df = (
        state_data
        .pipe(pipes.name_filter, st.session_state['name_filter'])
        .group_by('name', 'year')
        .agg(pl.col('count').sum())
        .sort(by=['name', 'year'])
        .collect(engine='streaming')
    )

    line_chart = px.line(
        data_frame=temp_df,
        x='year',
        y='count',
        color='name'
    )

    return line_chart