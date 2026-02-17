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


@st.cache_data
def load_unique_state_names():
    print('loading unique state names...')
    return (
        pl.read_parquet('data/state_data.parquet')
        .unique('name')
        .sort(by=['sex', 'name'])
        ['name']
        .to_list()
    )


@st.cache_data
def load_unique_national_names():
    print('loading unique national names...')
    return (
        pl.read_parquet('data/national_data.parquet')
        .unique('name')
        .sort(by=['sex', 'name'])
        ['name']
        .to_list()
    )