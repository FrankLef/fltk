from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from .main import CalcComb  # Only imported when checking types


def calculate(inst: CalcComb) -> pd.DataFrame:
    df = pd.merge(
        left=inst._valid_data,
        right=inst._combs_df,
        left_on=inst._data_idx,
        right_on=inst._idx_from,
    )
    df[inst._data_newvalue] = df[inst._comb_coef] * df[inst._data_value]
    sumkeys = inst._data_group.copy()
    sumkeys.append(inst._idx_to)
    calc_data = df.groupby(by=sumkeys, as_index=False)[inst._data_newvalue].sum()
    return calc_data
