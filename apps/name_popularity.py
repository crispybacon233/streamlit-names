import streamlit as st

import polars as pl

import plotly.express as px

import src.pipes as pipes
import src.widgets as widgets
import src.charts as charts
import src.utils as utils


utils.init_session_states()


widgets.name_select_single()


df = (
    pl.scan_parquet('data/state_data.parquet')
    .pipe(pipes.name_state_dist)
    .pipe(pipes.filter_name_single, st.session_state['names_filter_single'])
    .collect(engine='streaming')
)

st.write(df)