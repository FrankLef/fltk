from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from .main import CalcSumprod  # Only imported when checking types


def calculate(inst: CalcSumprod) -> pd.DataFrame:
    df = pd.merge(
        left=inst.valid,
        right=inst.sump,
        left_on=inst.raw_vars.idx,
        right_on=inst.sump_vars.idx_from,
    )
    df[inst.raw_vars.newvalue] = df[inst.sump_vars.sump_coef] * df[inst.raw_vars.value]
    # sumkeys = inst._data_group.copy()
    sumkeys = list(inst.raw_vars.groups)
    sumkeys.append(inst.sump_vars.idx_to)
    calc_data = df.groupby(by=sumkeys, as_index=False)[inst.raw_vars.newvalue].sum()
    return calc_data
