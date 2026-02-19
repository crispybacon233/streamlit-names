import streamlit as st
import polars as pl

import src.pipes as pipes
import src.widgets as widgets
import src.utils as utils
from src.charts import choropleth_name_dist, line_chart_single_name_count
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

        st.markdown('#### State Share Map')
        st.plotly_chart(choropleth_name_dist(), width='stretch')

        st.markdown('#### National Count Trend')
        st.plotly_chart(line_chart_single_name_count(), width='stretch')

        table_df = (
            name_dist_df
            .with_columns((pl.col('proportion') * 100).round(2).alias('share_pct'))
            .select(['state', 'count', 'share_pct'])
            .sort('share_pct', descending=True)
            .rename({'state': 'State', 'count': 'Births', 'share_pct': 'Share (%)'})
            .with_row_index(name='Rank', offset=1)
        )

        st.markdown('#### State Breakdown')
        st.dataframe(
            table_df,
            width='stretch',
            height=460,
            hide_index=True,
            column_config={
                'Rank': st.column_config.NumberColumn('Rank', format='%d', width='small'),
                'State': st.column_config.TextColumn('State', width='small'),
                'Births': st.column_config.NumberColumn('Births', format='%d', width='medium'),
                'Share (%)': st.column_config.NumberColumn(
                    'Share (%)',
                    format='%.2f%%',
                    width='large',
                ),
            },
        )
