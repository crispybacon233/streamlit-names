import streamlit as st
from src.widgets import year_range_slider


st.header('Top 10 Names by State')

year_range_slider()

st.write(st.session_state['year_range'])


