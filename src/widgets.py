import streamlit as st
from src.utils import load_unique_state_names


# load data for option values
NAME_OPTIONS = load_unique_state_names()


def year_range_slider():
    """
    Widget for selecting the year range filter.
    The filter is global.
    """

    if 'year_range' not in st.session_state:
        st.session_state.year_range = (1910, 2024)

    def update_range():
        st.session_state.year_range = st.session_state._temp_slider

    st.slider(
        'Select year range',
        min_value=1910, 
        max_value=2024,
        value=st.session_state.year_range,
        key='_temp_slider',
        on_change=update_range
    )


def name_select():
    if 'name_filter' not in st.session_state:
        st.session_state.name_filter = ['John - M', 'Mary - F']

    def update_names():
        st.session_state.name_filter = st.session_state._temp_name_filter

    st.multiselect('Select names', options=NAME_OPTIONS, key='_temp_name_filter', default=st.session_state.name_filter, on_change=update_names)