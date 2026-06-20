from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from .main import MungEwm  # Only imported when checking types


def get_ewm(inst: MungEwm) -> pd.DataFrame:
    _ewm = inst.ewm_vars
    _raw = inst.raw_vars

    data = inst.base.copy()

    for value in _raw.values:
        ewm_nm = value + "_" + _ewm.suffix
        # transform() returns a series aligned with the original DataFrame index. i.e. keep all original columns, just add the new ewm columns.
        data[ewm_nm] = data.groupby(list(_raw.groups))[value].transform(
            lambda x: x.ewm(span=_ewm.span).mean()
        )

    data_ordered = data.loc[inst.raw.index]

    return data_ordered
