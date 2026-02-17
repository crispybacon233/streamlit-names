import streamlit as st
import polars as pl

import plotly.express as px

import src.widgets as widgets
from src.charts import line_chart_name_counts


with st.popover('Filters'):
    widgets.year_range_slider()
    widgets.name_select()


st.plotly_chart(line_chart_name_counts(), width='content')