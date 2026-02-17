import streamlit as st
import src.widgets as widgets




widgets.year_range_slider()
st.write(st.session_state.year_range)