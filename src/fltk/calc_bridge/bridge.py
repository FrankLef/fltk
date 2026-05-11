from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

from ..utils import audit_vars as audit

if TYPE_CHECKING:
    from .main import CalcBridge  # Only imported when checking types


def get_bridge(inst: CalcBridge) -> pd.DataFrame:
    audit.audit_illegal(inst.raw, vars=inst.bridge_vars.vars)
    filtered_data = filter_data_with_ratios(inst)
    bridge_df = merge_data_with_periods(inst, data=filtered_data)
    return bridge_df


def filter_data_with_ratios(inst: CalcBridge) -> pd.DataFrame:
    data = inst.raw.copy()
    filtered_data = data[data[inst.raw_vars.ratio_nm].isin(inst.ratios)]
    return filtered_data


def merge_data_with_periods(inst: CalcBridge, data: pd.DataFrame) -> pd.DataFrame:
    _periods = inst.periods
    _period = inst.raw_vars.period
    _groups = inst.raw_vars.groups
    _ratio_nm = inst.raw_vars.ratio_nm
    _start = inst.periods_vars.start
    _end = inst.periods_vars.end

    data = data[list(inst.raw_vars.vars)]
    bridge_start = _periods.merge(
        right=data, how="inner", left_on=_start, right_on=_period
    )
    bridge_start.drop(columns=_period, inplace=True)

    bridge_end = _periods.merge(right=data, how="inner", left_on=_end, right_on=_period)
    bridge_end.drop(columns=[_period, _start], inplace=True)

    _on = (*_groups, _ratio_nm, _end)
    suffixes = inst.add_suffix("")
    bridge_df = bridge_start.merge(
        right=bridge_end, how="inner", on=_on, suffixes=suffixes
    )
    return bridge_df
