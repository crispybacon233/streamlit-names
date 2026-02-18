import streamlit as st
import polars as pl



@st.cache_data
def load_data(path):
    print(f'loading state data from {path}...')
    return pl.scan_parquet(path)


@st.cache_data
def load_unique_state_names():
    print('loading unique state names...')
    return (
        pl.scan_parquet('data/state_data.parquet')
        .unique('name')
        .sort(by=['sex', 'name'])
        .select("name")
        .collect(engine='streaming')
        .get_column('name')
        .to_list()
    )


@st.cache_data
def load_unique_national_names():
    print('loading unique national names...')
    return (
        pl.scan_parquet('data/national_data.parquet')
        .unique('name')
        .sort(by=['sex', 'name'])
        .select("name")
        .collect(engine='streaming')
        .get_column('name')
        .to_list()
    )


def init_session_states():
    if 'year_range' not in st.session_state:
        st.session_state.year_range = (1910, 2024)
    
    if 'names_filter_multi' not in st.session_state:
        st.session_state.names_filter_multi = ['John - M', 'Mary - F']

    if 'names_filter_single' not in st.session_state:
        st.session_state.names_filter_single = 'John - M'

    if 'sex' not in st.session_state:
        st.session_state.sex = 'M'