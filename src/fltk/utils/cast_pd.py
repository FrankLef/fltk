import pandas as pd
from typing import Iterable


def cast_pd_dtype(
    df: pd.Dataframe, from_dtypes: Iterable[str], to_dtype: str
) -> pd.Dataframe:
    """Cast pandas dtypes to a new dtype.

    Used often to solve conflict caused by the new str dtypes with pandas 3.0. Until dependencies are resolved in third-party libraries.
    """
    cols = df.select_dtypes(include=from_dtypes).columns
    for col in cols:
        df[col] = df[col].astype(to_dtype)
    return df
