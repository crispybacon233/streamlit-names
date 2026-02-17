import streamlit as st
import src.widgets as widgets
from src.utils import load_national_names, load_state_names, load_unique_state_names



# Load data
national_data = load_national_names()
state_data = load_state_names()
name_options = load_unique_state_names()



widgets.year_range_slider()

st.multiselect('Select names', options=name_options)

st.write(st.session_state.year_range)