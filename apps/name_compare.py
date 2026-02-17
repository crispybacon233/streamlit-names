import streamlit as st
import polars as pl

import plotly.express as px

import src.widgets as widgets
from src.charts import line_chart_name_counts


st.header('Name Compare')

with st.popover('Filters'):
    widgets.name_select()
    widgets.metric_radio()


if st.session_state.name_filter:
    st.plotly_chart(line_chart_name_counts(), width='content')
else:
    st.write('Use filter to choose names!')