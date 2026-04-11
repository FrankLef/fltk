from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from .main import CalcSumprod  # Only imported when checking types


def add_calc(inst: CalcSumprod) -> pd.DataFrame:
    newvalue=inst._data_newvalue
    
    left_on = inst._data_group.copy()
    left_on.append(inst._data_idx)
    left_df = inst._valid_data
    
    right_on = inst._data_group.copy()
    right_on.append(inst._idx_to)
    right_cols = right_on.copy()
    right_cols.append(newvalue)
    right_df = inst._calc_data[right_cols]
    
    if newvalue in left_df.columns:
        left_df.drop(columns=[newvalue], inplace=True)
    data = pd.merge(left=left_df, right=right_df, how="left", left_on=left_on, right_on=right_on)
    if data.empty:
        msg: str = "`add_calc()` returned an empty dataframe. Are the keys ok?"
        raise AssertionError(msg)
    return data
