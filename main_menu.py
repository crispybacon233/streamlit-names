import streamlit as st

apps = {
    'Name Trends': [st.Page('apps/name_trends.py', title="Name Trends")],
    "By State": [
        st.Page("apps/top_10_state.py", title="Top 10 Names by State"),
    ],
}

pg = st.navigation(apps)
pg.run()