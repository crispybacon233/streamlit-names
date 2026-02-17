import streamlit as st

apps = {
    'Name Trends': [st.Page('apps/name_compare.py', title="Name Compare")],
    "By State": [
        st.Page("apps/top_10_state.py", title="Top 10 Names by State"),
    ],
}

pg = st.navigation(apps)
pg.run()