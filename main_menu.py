import streamlit as st

st.set_page_config(layout='wide')

apps = {
    "By State": [
        st.Page('apps/top_10_state.py', title='Top 10 Names by State'),
        st.Page('apps/name_popularity.py', title='How Popular is Your Name?')
    ],
    'Name Trends': [st.Page('apps/name_compare.py', title='Name Compare')],
}

pg = st.navigation(apps)
pg.run()