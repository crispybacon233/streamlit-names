import streamlit as st
import src.widgets as widgets
import src.pipes as pipes
from src.utils import load_national_names, load_state_names, load_unique_state_names



# Load data
national_data = load_national_names()
state_data = load_state_names()
name_options = load_unique_state_names()



widgets.year_range_slider()
widgets.name_select()

temp_df = (
    state_data
    .pipe(pipes.filter_year, st.session_state['year_range'])
)
st.dataframe(temp_df.head(500))