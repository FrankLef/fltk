from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING, Final
import pandas as pd

if TYPE_CHECKING:
    from .diffmat import DiffMat  # Only imported when checking types


def get_valid_data(inst: DiffMat) -> pd.DataFrame:
    keys = inst._data_keys
    valid_data = inst._data
    dfs = [inst._invalid_data, inst._undetermined_data]
    for df in dfs:
        right_df = df[keys]
        valid_data = clean_data(left_df=valid_data, right_df=right_df, keys=keys)

    ndata: int = inst._data.shape[0]
    ninvalid: int = inst._invalid_data.shape[0]
    nundetermined = inst._undetermined_data.shape[0]
    nvalid: int = valid_data.shape[0]
    ncheck: int = ndata - ninvalid - nundetermined
    if nvalid != ncheck:
        msg: str = f"There must be {ncheck}={ndata}-{ninvalid}-{nundetermined} rows in the valid data."
        raise AssertionError(msg)
    return valid_data


def clean_data(
    left_df: pd.DataFrame, right_df: pd.DataFrame, keys: list[str]
) -> pd.DataFrame:
    MERGE: Final[str] = "_merge"
    HOW_LEFT: Final[str] = "left"
    LEFT_ONLY: Final[str] = "left_only"
    merged_df = pd.merge(
        left=left_df,
        right=right_df,
        left_on=keys,
        right_on=keys,
        how=HOW_LEFT,
        indicator=True,
    )
    if merged_df.empty:
        msg = "The merged_df is empty."
        raise AssertionError(msg)
    clean_data_df = merged_df.loc[merged_df._merge == LEFT_ONLY]
    clean_data_df.drop(columns=[MERGE], inplace=True)
    return clean_data_df
