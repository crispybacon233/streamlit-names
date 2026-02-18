import streamlit as st

from src.utils import apply_base_style

import src.widgets as widgets
from src.charts import line_chart_name_counts


###############
# LAYOUT
###############
apply_base_style()
st.title('Name Compare')
st.markdown(
    "<p class='dashboard-subtitle'>Compare historical popularity trends for multiple names.</p>",
    unsafe_allow_html=True,
)

filter_col, chart_col = st.columns([1.2, 3.8])

###############
# FILTERS
###############
with filter_col:
    with st.container(border=True):
        widgets.name_select_multi()
        st.divider()
        widgets.metric_radio()

###############
# LINE CHART
###############
with chart_col:
    if st.session_state['names_filter_multi']:
        st.plotly_chart(line_chart_name_counts(), width='stretch')
    else:
        st.info('Use the filter panel to choose one or more names.')
