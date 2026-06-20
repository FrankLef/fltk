from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from .main import CalcSumprod  # Only imported when checking types


def add_calc(inst: CalcSumprod) -> pd.DataFrame:
    newvalue = inst.raw_vars.newvalue

    left_on = list(inst.raw_vars.groups)
    left_on.append(inst.raw_vars.idx)
    left_df = inst.valid

    right_on = list(inst.raw_vars.groups)
    right_on.append(inst.sump_vars.idx_to)
    right_cols = right_on.copy()
    right_cols.append(newvalue)
    right_df = inst.calc[right_cols]

    if newvalue in left_df.columns:
        left_df.drop(columns=[newvalue], inplace=True)
    data = pd.merge(
        left=left_df, right=right_df, how="left", left_on=left_on, right_on=right_on
    )
    if data.empty:
        msg: str = "`add_calc()` returned an empty dataframe. Are the keys ok?"
        raise AssertionError(msg)
    return data
