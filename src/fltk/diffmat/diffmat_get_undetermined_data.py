from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING, Final
import pandas as pd

if TYPE_CHECKING:
    from .diffmat import DiffMat  # Only imported when checking types


def get_undetermined_data(inst: DiffMat) -> pd.DataFrame:
    MERGE: Final[str] = "_merge"
    HOW_LEFT: Final[str] = "left"
    MERGE_BOTH: Final[str] = "both"
    left_df = inst._data
    right_df = inst._idx_df
    left_on = inst._data_idx
    right_on = inst._idx_to
    merged_df = pd.merge(
        left_df,
        right_df,
        left_on=left_on,
        right_on=right_on,
        how=HOW_LEFT,
        indicator=True,
    )
    if merged_df.empty:
        msg = "The merged_df is empty."
        raise AssertionError(msg)
    # print("\nundetermined_data, merged_df:\n", merged_df)
    undetermined_data = merged_df.loc[merged_df[MERGE] != MERGE_BOTH]
    undetermined_data.drop(columns=[MERGE], inplace=True)
    # print("columns:", undetermined_data.columns)
    undetermined_data = undetermined_data[inst._data_keys]
    # print("\nundetermined_data:\n", undetermined_data)
    return undetermined_data
