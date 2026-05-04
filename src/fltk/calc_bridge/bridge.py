from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from .main import CalcBridge  # Only imported when checking types


def get_bridge(inst: CalcBridge) -> pd.DataFrame:
    _raw = inst.raw_df
    _periods = inst.periods_df
    _period = inst.raw.period
    _groups = inst.raw.groups
    _ratio_nm = inst.raw.ratio
    _start = inst.periods.start
    _end = inst.periods.end

    data = _raw[list(inst.raw.vars)]
    bridge_start = _periods.merge(
        right=data, how="inner", left_on=_start, right_on=_period
    )
    bridge_start.drop(columns=_period, inplace=True)

    bridge_end = _periods.merge(right=data, how="inner", left_on=_end, right_on=_period)
    bridge_end.drop(columns=[_period, _start], inplace=True)

    _on = (*_groups, _ratio_nm, _end)
    suffixes = ("_" + inst.bridge.from_sfx, "_" + inst.bridge.to_sfx)
    bridge_df = bridge_start.merge(
        right=bridge_end, how="inner", on=_on, suffixes=suffixes
    )
    # breakpoint()
    return bridge_df
