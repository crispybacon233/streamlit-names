import streamlit as st
import polars as pl
import plotly.express as px


import src.pipes as pipes
from src.utils import load_data


# Load data
national_data = load_data('data/national_data.parquet')
state_data = load_data('data/state_data.parquet')


def line_chart_name_counts():
    # define vars
    metric = st.session_state['metric']
    if metric == 'rank':
        y = 'rank'
    else:
        y = 'count'

    temp_df = (
        national_data
        .pipe(pipes.filter_names_multi, st.session_state['names_filter_multi'])
        .sort(by=['name', 'year'])
        .collect(engine='streaming')
    )

    line_chart = px.line(
        data_frame=temp_df,
        x='year',
        y=y,
        color='name',
        custom_data=['name', 'count', 'rank'],
    ).update_traces(
        hovertemplate=(
            "<b>count: %{customdata[1]}</b><br>" +
            "<b>rank: %{customdata[2]}</b>"
            )
    ).update_layout(
        hovermode='x unified',
        template='plotly_white',
        margin=dict(l=20, r=20, t=30, b=20),
        legend_title_text='',
        xaxis_title='Year',
        yaxis_title='Birth count' if metric != 'rank' else 'Rank',
    )

    if metric == 'rank':
        line_chart.update_yaxes(autorange="reversed")
    if metric == 'logarithm':
        line_chart.update_yaxes(type="log")

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
            "<b>%{location}</b><br>" +
            "%{customdata[0]}" +
            "<extra></extra>"
        )
    )

    top_10_fig.update_layout(
        height=620,
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor=bgcolor,
        plot_bgcolor=bgcolor,
    )

    top_10_fig.update_geos(bgcolor=bgcolor)

    return top_10_fig


def choropleth_name_dist():
    selected_name = st.session_state['names_filter_single']

    temp_df = (
        state_data
        .pipe(pipes.name_state_dist)
        .pipe(pipes.filter_name_single, selected_name)
        .with_columns((pl.col('proportion') * 100).round(2).alias('proportion_pct'))
        .collect(engine='streaming')
    )

    name_dist_fig = px.choropleth(
        temp_df,
        locations='state',
        locationmode='USA-states',
        scope='usa',
        color='proportion',
        color_continuous_scale='Blues',
        custom_data=['count', 'proportion_pct'],
    )

    name_dist_fig.update_traces(
        hovertemplate=(
            f"<b>%{{location}}</b><br>"
            f"{selected_name}<br>"
            "Count: %{customdata[0]}<br>"
            "Proportion: %{customdata[1]}%"
            "<extra></extra>"
        )
    )

    name_dist_fig.update_layout(
        template='plotly_white',
        height=520,
        margin=dict(l=20, r=20, t=20, b=20),
        coloraxis_colorbar=dict(title='Share'),
    )

    return name_dist_fig
