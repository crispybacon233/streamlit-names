import streamlit as st
from src.widgets import year_range_slider

if 'year_range' not in st.session_state:
    st.session_state.year_range = (1910, 2024)


year_range_slider()
st.write(st.session_state.year_range)