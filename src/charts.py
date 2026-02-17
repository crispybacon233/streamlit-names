import streamlit as st
import polars as pl
import plotly.express as px


import src.pipes as pipes
from src.utils import load_data


# Load data
national_data = load_data('data/national_data.parquet')
state_data = load_data('data/state_data.parquet')


def line_chart_name_counts():

    metric = st.session_state['metric']

    temp_df = (
        national_data
        .pipe(pipes.rank_names, metric)
        .pipe(pipes.filter_name, st.session_state['name_filter'])
        .sort(by=['name', 'year'])
        .collect(engine='streaming')
    )

    if st.session_state['metric'] == 'rank':
        y = 'rank'
    else:
        y = 'count'

    line_chart = px.line(
        data_frame=temp_df,
        x='year',
        y=y,
        color='name'
    )

    if metric == 'rank':
        line_chart.update_yaxes(autorange="reversed")
    if metric == 'logarithm':
        line_chart.update_layout(yaxis_type="log")

    return line_chart


def choropleth_top_10_by_state():
    # define vars
    if st.session_state.sex == 'F':
        sex_color = '#F88379'
        bgcolor = '#FADADD'
    if st.session_state.sex == 'M':
        sex_color = '#636EFA'
        bgcolor = '#90D5FF'

    start_year = st.session_state.year_range[0]
    end_year = st.session_state.year_range[1]


    top_10_by_state = (
        state_data
        .pipe(pipes.filter_year, st.session_state['year_range'])
        .pipe(pipes.filter_sex, st.session_state['sex'])
        .pipe(pipes.top_10_state)
        .sort('rank')
    )

    # Aggregate to one row per state
    hover_df = (
        top_10_by_state
        .with_columns(
            formatted_label = (
                pl.col("rank").cast(pl.Utf8) + ". " + 
                pl.col("name") + " (" + 
                pl.col("count").cast(pl.Utf8) + ")"
            )
        )
        .group_by("state")
        .agg(all_names = pl.col("formatted_label").str.join("<br>"))
    )


    # 1. Get the #1 name for each state to use as a label
    number_one_names = (
        top_10_by_state
        .filter(pl.col("rank") == 1)
        .select("state", "name")
        .rename({"name": "top_1_name"})
    )

    # 2. Join it back to your aggregated hover data
    final_df = hover_df.join(number_one_names, on="state").collect(engine='streaming')

    top_10_fig = px.choropleth(
        final_df,
        locations='state',
        locationmode='USA-states',
        scope='usa',
        color_discrete_sequence=[sex_color],
        custom_data=['all_names'],
    )

    # 2. Add the labels (The text layer)
    top_10_fig.add_scattergeo(
        locations=final_df['state'],
        locationmode='USA-states',
        text=final_df['top_1_name'],
        mode='text',
        hoverinfo='skip', # We want the choropleth layer to handle hovers
        textfont=dict(size=10, color="white")
    )

    # 3. Apply your hover template to the choropleth layer
    top_10_fig.update_traces(
        selector=dict(type='choropleth'),
        hovertemplate=(
            "<b>State: %{location}</b><br><br>" +
            "<b>Top 10:</b><br>%{customdata[0]}" +
            "<extra></extra>"
        )
    )

    top_10_fig.update_layout(
        width=1000,
        height=600,
        showlegend=False,
        paper_bgcolor=bgcolor
    )

    top_10_fig.update_geos(bgcolor=bgcolor)

    return top_10_fig