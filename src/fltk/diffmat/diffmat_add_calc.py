from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING, Final
import pandas as pd

if TYPE_CHECKING:
    from .diffmat import DiffMat  # Only imported when checking types


def add_calc(inst: DiffMat) -> pd.DataFrame:
    HOW: Final[str] = "left"
    newvalue = inst._data_newvalue
    keys: list[str] = inst._data_keys.copy()
    right_cols = keys.copy()
    right_cols.append(newvalue)
    left_df = inst._data
    right_df = inst._valid_data[right_cols]
    if newvalue in left_df.columns:
        left_df.drop(columns=[newvalue], inplace=True)
    data = pd.merge(left=left_df, right=right_df, how=HOW, on=keys)

    nna = data[newvalue].isna().sum()
    ninvalid = inst._data.shape[0] - inst._valid_data.shape[0]
    if nna != ninvalid:
        msg: str = f"The number of NaN is {nna}, it must be {ninvalid}."
        raise AssertionError(msg)
    return data
