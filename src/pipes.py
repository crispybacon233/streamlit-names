import polars as pl
from typing import List, Tuple


def filter_year(df: pl.LazyFrame, year_range: Tuple[int]) -> pl.LazyFrame:
    """
    Filters for years between range.
    
    Args:
        df (polars LazyFrame): Names data.
        year_range (tuple): Tuple of year range.

    Returns:
        pl.LazyFrame: The filtered LazyFrame.
    """

    return df.filter(pl.col('year').is_between(year_range[0], year_range[1]))


def filter_names_multi(df: pl.LazyFrame, names_filter_multi: List[str]) -> pl.LazyFrame:
    """
    Filters for names in list.
    
    Args:
        df (polars LazyFrame): Names data.
        names_filter_multi (List[str]): List of names.

    Returns:
        pl.LazyFrame: The filtered LazyFrame.
    """

    return df.filter(pl.col('name').is_in(names_filter_multi))


def filter_name_single(df: pl.LazyFrame, names_filter_single: str) -> pl.LazyFrame:
    """
    Filters for single name.
    
    Args:
        df (polars LazyFrame): Names data.
        name_filter (List[str]): List of names.

    Returns:
        pl.LazyFrame: The filtered LazyFrame.
    """

    return df.filter(pl.col('name') == names_filter_single)



def filter_sex(df: pl.LazyFrame, sex: str) -> pl.LazyFrame:
    """
    Filters for sex.
    
    Args:
        df (polars LazyFrame): Names data.
        sexs_filter str: Chosen sex.

    Returns:
        pl.LazyFrame: The filtered LazyFrame.
    """
    return df.filter(pl.col('sex') == sex)


def rank_names(df: pl.LazyFrame, metric: str) -> pl.LazyFrame:
    """
    If metric is set to 'rank', calculate the ranks for each name.
    """
    if metric == 'rank':
        df = (
            df
            .with_columns(
                pl.col('count')
                .rank(descending=True, method='dense') 
                .over('year', 'sex')
                .alias('rank')
            )
        )
    return df


def top_10_state(df: pl.LazyFrame) -> pl.LazyFrame:
    """
    Aggregates the name counts by state then filters for top 10 within a year range.
    """
    return (
        df
        .group_by('state', 'name', 'sex')
        .agg(pl.col('count').sum())
        .with_columns(
            pl.col('count').rank(method='ordinal', descending=True).over('state').alias('rank')
        )
        .filter(pl.col('rank') <= 10)
    )


def name_state_dist(df: pl.LazyFrame) -> pl.LazyFrame:
    return (
        df
        .group_by('state', 'name')
        .agg(pl.col('count').sum())
        .with_columns(
            (pl.col("count") / pl.col("count").sum().over("state")).alias("proportion")
        )
    )