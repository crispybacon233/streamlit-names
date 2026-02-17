import streamlit as st
import polars as pl

import plotly.express as px

import src.widgets as widgets
from src.charts import line_chart_name_counts


###############
# LAYOUT
###############
st.header('Name Compare')

name_select_col, metric_col, chart_col = st.columns([2, 1, 11])


###############
# FILTERS
###############
# with st.popover('Filters'):
with name_select_col:
    widgets.name_select()
with metric_col:
    widgets.metric_radio()


###############
# LINE CHART
###############
if st.session_state.name_filter:
    with chart_col:
        st.plotly_chart(line_chart_name_counts())
else:
    st.write('Use filter to choose names!')