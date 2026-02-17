import streamlit as st
import polars as pl


@st.cache_data
def load_state_names():
    print('loading state data...')
    return pl.read_parquet('data/state_data.parquet')


@st.cache_data
def load_national_names():
    print('loading national data...')
    return pl.read_parquet('data/national_data.parquet')