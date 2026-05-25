from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from .main import CalcEwm  # Only imported when checking types


def get_ewm(inst: CalcEwm) -> pd.DataFrame:
    _ewm = inst.ewm_vars
    _raw = inst.raw_vars

    data = inst.base.copy()

    print("inside get_ewm:", _raw.values_ewm)

    for value_nm, ewm_nm in _raw.values_ewm.items():
        # print("inside get_ewm")
        # print("value_nm:", value_nm, ";", "ewm_nm:", ewm_nm)
        # transform() returns a series aligned with the original DataFrame index. i.e. keep all original columns, just add the new ewm columns.
        data[ewm_nm] = data.groupby(list(_raw.groups))[value_nm].transform(
            lambda x: x.ewm(span=_ewm.span).mean()
        )

    data.sort_values(list(_raw.keys), ascending=True, inplace=True)

    return data
