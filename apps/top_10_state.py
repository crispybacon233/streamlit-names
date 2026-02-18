import streamlit as st

from src.utils import load_data, init_session_states, apply_base_style
from src.charts import choropleth_top_10_by_state
import src.widgets as widgets


###############
# SESSIONS & DATA
###############
apply_base_style()
init_session_states()
load_data('data/state_data.parquet')

sex_title = 'Female' if st.session_state.sex == 'F' else 'Male'
start_year, end_year = st.session_state.year_range

###############
# HEADER
###############
st.title('Top 10 Names by State')
if start_year == end_year:
    st.markdown(
        f"<p class='dashboard-subtitle'>Showing <b>{sex_title}</b> baby names for <b>{start_year}</b>.</p>",
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        (
            "<p class='dashboard-subtitle'>"
            f"Showing <b>{sex_title}</b> baby names from <b>{start_year}</b> to <b>{end_year}</b>."
            "</p>"
        ),
        unsafe_allow_html=True,
    )

###############
# FILTERS
###############
filter_col_1, filter_col_2 = st.columns([1.2, 3])

with filter_col_1:
    with st.container(border=True):
        widgets.sex_radio()

with filter_col_2:
    with st.container(border=True):
        widgets.year_range_slider()

###############
# US MAP
###############
st.plotly_chart(choropleth_top_10_by_state(), width='stretch')
