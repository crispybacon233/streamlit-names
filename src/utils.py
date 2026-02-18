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


def apply_base_style():
    """Applies a consistent, dashboard-like visual style across pages."""

    st.markdown(
        """
        <style>
            .block-container {
                padding-top: 1.5rem;
                padding-bottom: 1rem;
                max-width: 1300px;
            }
            [data-testid="stMetricValue"] {
                font-size: 1.8rem;
            }
            .dashboard-subtitle {
                color: #6b7280;
                margin-top: -0.35rem;
                margin-bottom: 1rem;
                font-size: 0.95rem;
            }
            .panel {
                border: 1px solid #e5e7eb;
                border-radius: 12px;
                padding: 0.75rem 0.9rem;
                background: #ffffff;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
