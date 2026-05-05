from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from .main import CalcSumprod  # Only imported when checking types


def get_valid_data(inst: CalcSumprod) -> pd.DataFrame:
    keys = inst._data_keys
    data = inst._data
    invalid_dfs: tuple[pd.DataFrame, ...] = (inst._invalid_data,)
    for invalid_df in invalid_dfs:
        if not invalid_df.empty:
            right_df = invalid_df[keys]
            valid_data = clean_data(left_df=data, right_df=right_df, keys=keys)
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


def fill_na(inst: CalcSumprod, value: float = 0) -> pd.DataFrame:
    valid_data = inst._data.copy()
    # NOTE: Error msg from pandas, use this command instead of next one
    valid_data.fillna({inst._data_value: value}, inplace=True)
    # valid_data[inst._data_value].fillna(value=value, inplace=True)
    return valid_data
