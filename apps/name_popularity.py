import streamlit as st
import polars as pl

import src.pipes as pipes
import src.widgets as widgets
import src.utils as utils
from src.charts import choropleth_name_dist
from src.utils import apply_base_style


###############
# SESSIONS
###############
apply_base_style()
utils.init_session_states()


###############
# HEADER
###############
st.title('How Popular is Your Name?')
st.markdown(
    "<p class='dashboard-subtitle'>See where a name is most common based on proportional share within each state.</p>",
    unsafe_allow_html=True,
)


###############
# FILTERS
###############
filter_col, content_col = st.columns([1.3, 3.7])

with filter_col:
    with st.container(border=True):
        widgets.name_select_single()


###############
# DATA
###############
selected_name = st.session_state['names_filter_single']

name_dist_df = (
    pl.scan_parquet('data/state_data.parquet')
    .pipe(pipes.name_state_dist)
    .pipe(pipes.filter_name_single, selected_name)
    .sort('proportion', descending=True)
    .collect(engine='streaming')
)


###############
# CONTENT
###############
with content_col:
    if name_dist_df.height == 0:
        st.warning('No records found for this name.')
    else:
        top_state = name_dist_df.row(0, named=True)

        metric_col1, metric_col2, metric_col3 = st.columns(3)
        metric_col1.metric('Selected Name', selected_name)
        metric_col2.metric('Top State', top_state['state'])
        metric_col3.metric('Top Share', f"{top_state['proportion'] * 100:.2f}%")

        st.plotly_chart(choropleth_name_dist(), width='stretch')

        st.dataframe(
            name_dist_df.with_columns((pl.col('proportion') * 100).round(2).alias('share_pct'))
            .select(['state', 'count', 'share_pct'])
            .rename({'count': 'total_births', 'share_pct': 'share_%'}),
            width='stretch',
            height=420,
        )
