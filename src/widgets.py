import streamlit as st


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
        1910, 2024,
        value=st.session_state.year_range,
        key='_temp_slider',
        on_change=update_range
    )