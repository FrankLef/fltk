from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from .main import CalcBridge  # Only imported when checking types


def get_bridge(inst: CalcBridge) -> pd.DataFrame:
    validate_vars(inst)
    bridge_df = get_data(inst)
    return bridge_df


def validate_vars(inst: CalcBridge) -> None:
    """Validate that no bridge variable is used by raw data."""
    _raw_vars = inst.raw_vars.vars
    _bridge_vars = inst.bridge_vars.vars

    invalid_vars = [var for var in _raw_vars if var in _bridge_vars]
    if invalid_vars:
        msg: str = f"{invalid_vars} are found in raw and bridge."
        raise KeyError(msg)


def get_data(inst: CalcBridge) -> pd.DataFrame:
    _raw = inst.raw
    _periods = inst.periods
    _period = inst.raw_vars.period
    _groups = inst.raw_vars.groups
    _ratio_nm = inst.raw_vars.ratio_nm
    _start = inst.periods_vars.start
    _end = inst.periods_vars.end

    data = _raw[list(inst.raw_vars.vars)]
    bridge_start = _periods.merge(
        right=data, how="inner", left_on=_start, right_on=_period
    )
    bridge_start.drop(columns=_period, inplace=True)

    bridge_end = _periods.merge(right=data, how="inner", left_on=_end, right_on=_period)
    bridge_end.drop(columns=[_period, _start], inplace=True)

    _on = (*_groups, _ratio_nm, _end)
    suffixes = inst.add_suffix("")
    # suffixes = ("_" + inst.bridge_vars.from_sfx, "_" + inst.bridge_vars.to_sfx)
    bridge_df = bridge_start.merge(
        right=bridge_end, how="inner", on=_on, suffixes=suffixes
    )
    return bridge_df
