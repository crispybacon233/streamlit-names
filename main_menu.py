import streamlit as st

from src.utils import apply_base_style

st.set_page_config(
    page_title='US Baby Names Dashboard',
    page_icon='📊',
    layout='wide',
    initial_sidebar_state='expanded',
)
apply_base_style()

st.title('US Baby Names Dashboard')
st.caption('Explore historical naming trends across the United States.')

apps = {
    'By State': [
        st.Page('apps/name_popularity.py', title='How Popular is Your Name?', icon='📍'),
        st.Page('apps/top_10_state.py', title='Top 10 Names by State', icon='🗺️'),
    ],
    'Name Trends': [st.Page('apps/name_compare.py', title='Name Compare', icon='📈')],
}

pg = st.navigation(apps)
pg.run()
