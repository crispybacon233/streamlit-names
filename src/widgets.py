import streamlit as st
from src.utils import load_unique_state_names, load_unique_national_names


# load data for option values
NAME_OPTIONS_STATE = load_unique_state_names()
NAME_OPTIONS_NATIONAL = load_unique_national_names()


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
        'Year range',
        min_value=1910, 
        max_value=2024,
        value=st.session_state.year_range,
        key='_temp_slider',
        on_change=update_range
    )


def name_select_multi():
    """
    Widget for selecting names filter.
    """

    if 'names_filter_multi' not in st.session_state:
        st.session_state.names_filter_multi = ['John - M', 'Mary - F']

    def update_names():
        st.session_state.names_filter_multi = st.session_state._temp_names_filter_multi

    st.multiselect(
        'Names to compare', 
        options=NAME_OPTIONS_STATE, 
        key='_temp_names_filter_multi', 
        default=st.session_state.names_filter_multi, 
        on_change=update_names
    )


def name_select_single():
    """
    Widget for selecting a single name filter.
    """

    if 'names_filter_single' not in st.session_state:
        st.session_state.names_filter_single = 'Emmaline - F'

    def update_name():
        st.session_state.names_filter_single = st.session_state._temp_names_filter_single
    
    st.selectbox(
        'Choose Name', 
        options=NAME_OPTIONS_STATE, 
        key='_temp_names_filter_single', 
        index=NAME_OPTIONS_STATE.index(st.session_state.names_filter_single), 
        on_change=update_name
    )


def sex_radio():
    """
    Widget for selecting sex.
    """

    options = ['M', 'F']

    if 'sex' not in st.session_state:
        st.session_state.sex = options[0]

    def update_sex():
        st.session_state.sex = st.session_state._temp_sex

    st.radio(
        'Sex',
        options=['M', 'F'],
        key='_temp_sex',
        index=options.index(st.session_state.sex),
        on_change=update_sex,
        horizontal=True,
    )


def metric_radio():
    """
    Widget for choosing comparison metric (count, rank, logarithmic)
    """
    options = ['count', 'rank', 'logarithm']

    if 'metric' not in st.session_state:
        st.session_state.metric = options[0]

    def update_metric():
        st.session_state.metric = st.session_state._temp_metric

    st.radio(
        'Metric',
        options=options,
        key='_temp_metric',
        index=options.index(st.session_state.metric),
        on_change=update_metric,
        horizontal=True,
    )
