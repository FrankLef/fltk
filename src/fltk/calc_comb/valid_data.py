from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from .main import CalcComb  # Only imported when checking types


def get_valid_data(inst: CalcComb) -> pd.DataFrame:
    keys = inst._data_keys
    valid_data = inst._data
    dfs: list[pd.DataFrame] = [inst._invalid_data]
    for df in dfs:
        if not df.empty:
            right_df = df[keys]
            valid_data = clean_data(left_df=valid_data, right_df=right_df, keys=keys)
    return valid_data


def clean_data(
    left_df: pd.DataFrame, right_df: pd.DataFrame, keys: list[str]
) -> pd.DataFrame:
    merged_df = pd.merge(
        left=left_df,
        right=right_df,
        left_on=keys,
        right_on=keys,
        how="left",
        indicator=True,
    )
    if merged_df.empty:
        raise AssertionError("The merged_df is empty.")
    clean_data_df = merged_df.loc[merged_df._merge == "left_only"]
    clean_data_df.drop(columns=["_merge"], inplace=True)
    return clean_data_df
