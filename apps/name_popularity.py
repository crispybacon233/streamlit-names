import streamlit as st

import polars as pl

import plotly.express as px

import src.pipes as pipes
import src.widgets as widgets
import src.charts as charts


widgets.name_select_multi()


df = (
    pl.scan_parquet('data/state_data.parquet')
    .pipe(pipes.name_state_dist)
    .pipe(pipes.filter_names, st.session_state['names_filter_multi'])
    .collect(engine='streaming')
)

st.write(df)