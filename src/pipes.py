import polars as pl
from typing import List, Tuple


def filter_year(df: pl.DataFrame, year_range: Tuple[int]) -> pl.DataFrame:
    """
    Filters for years between range.
    
    Args:
        df (polars DataFrame): Names data.
        year_range (tuple): Tuple of year range.

    Returns:
        pl.DataFrame: The filtered DataFrame.
    """

    return df.filter(pl.col('year').is_between(year_range[0], year_range[1]))


def name_filter(df: pl.DataFrame, name_filter: List[str]) -> pl.DataFrame:
    """
    Filters for names in list.
    
    Args:
        df (polars DataFrame): Names data.
        name_filter (List[str]): List of names.

    Returns:
        pl.DataFrame: The filtered DataFrame.
    """

    return df.filter(pl.col('name').is_in(name_filter))
