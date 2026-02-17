import streamlit as st
import polars as pl


@st.cache_data
def load_state_data():
    print('loading state data...')
    return pl.read_parquet('data/state_data.parquet')


@st.cache_data
def load_national_data():
    print('loading national data...')
    return pl.read_parquet('data/national_data.parquet')


@st.cache_data
def load_unique_state_names():
    print('loading unique state names...')
    return (
        pl.read_parquet('data/state_data.parquet')
        .unique('name')
        .sort(by=['sex', 'name'])
        .get_column("name")
        .to_list()
    )


@st.cache_data
def load_unique_national_names():
    print('loading unique national names...')
    return (
        pl.read_parquet('data/national_data.parquet')
        .unique('name')
        .sort(by=['sex', 'name'])
        .get_column("name")
        .to_list()
    )


def init_session_states():
    if 'year_range' not in st.session_state:
        st.session_state.year_range = (1910, 2024)
    
    if 'name_filter' not in st.session_state:
        st.session_state.name_filter = ['John - M', 'Mary - F']