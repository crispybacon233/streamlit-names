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
