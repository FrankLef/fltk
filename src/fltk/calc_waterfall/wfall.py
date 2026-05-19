from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING, Final
import pandas as pd

if TYPE_CHECKING:
    from .main import CalcWaterfall  # Only imported when checking types


def get_wfall(inst: CalcWaterfall) -> pd.DataFrame:
    _wfall = inst.wfall_vars
    _raw = inst.raw_vars
    _initial = _wfall.initial
    _is_initial = _wfall.is_initial
    _keys = list(_raw.groups) + [_raw.ratio_nm]
    _order = list(_raw.groups) + [
        _raw.ratio_nm,
        _raw.period_from,
        _raw.period_to,
        _wfall.diff_nm,
    ]

    wfall = inst.base.copy()

    # NOTE: groupby() works reliably when you collect indexes. I wasted many hours trying to figure out what was going on.
    initial_ndx = []
    for _, group in wfall.groupby(_keys):
        group = set_initial(inst, group=group)
        initial_ndx.extend(group.index)
    wfall.loc[initial_ndx, _is_initial] = True

    wfall = rm_num_from(inst, data=wfall)
    wfall = rm_total_diff(inst, data=wfall)
    wfall = set_wfall_amt(inst, data=wfall)
    wfall = reset_initial(inst, data=wfall, initial=_initial)
    wfall.sort_values(by=_order, inplace=True)
    return wfall


def set_initial(inst: CalcWaterfall, group: pd.DataFrame) -> pd.DataFrame:
    """Set initial 'num_from_val'."""
    _raw = inst.raw_vars
    _period = _raw.period_to
    _num_from = _raw.num_from_val
    _wfall = inst.wfall_vars
    _diff_nm = _wfall.diff_nm

    period_sel = group[_period] == group[_period].min()
    num_sel = group[_diff_nm] == _num_from
    sel = period_sel & num_sel
    group_sel = group.loc[sel]
    return group_sel


def rm_num_from(inst: CalcWaterfall, data: pd.DataFrame) -> pd.DataFrame:
    """Remove all othe num_from_val not identified as 'initial'."""
    _raw = inst.raw_vars
    _num_from = _raw.num_from_val
    _wfall = inst.wfall_vars
    _diff_nm = _wfall.diff_nm
    _is_initial = _wfall.is_initial

    initial_sel = ~data[_is_initial]
    num_sel = data[_diff_nm] == _num_from
    data_sel = data.loc[initial_sel & num_sel]
    data.drop(index=data_sel.index, inplace=True)
    return data


def rm_total_diff(inst: CalcWaterfall, data: pd.DataFrame) -> pd.DataFrame:
    """Remove rows with 'total_diff' from the data."""
    _diff_nm = inst.wfall_vars.diff_nm
    _total_diff = inst.raw_vars.total_diff
    sel = data[_diff_nm] != _total_diff
    data = data.loc[sel]
    return data


def set_wfall_amt(inst: CalcWaterfall, data: pd.DataFrame) -> pd.DataFrame:
    """Total amount must be set to None (or zero)."""
    TOTAL: Final[str] = "total"
    _wfall = inst.wfall_vars
    _wfall_amt = _wfall.wfall_amt
    _diff_val = _wfall.diff_val
    _wtype = _wfall.wfall_type
    data[_wfall_amt] = data[_diff_val]
    sel = data[_wtype].astype(str) == TOTAL
    data.loc[sel, _wfall_amt] = None
    return data


def reset_initial(
    inst: CalcWaterfall, data: pd.DataFrame, initial: str
) -> pd.DataFrame:
    """Reset initial rows to 'absolute' or 'relative'.

    The first column in a waterfall can be shown as absolute or relative. This
    function reset initial to reflect that choice.

    Args:
        inst (CalcWaterfall): CalcWaterfall instance.
        data (pd.DataFrame): Waterfall data.
        initial (str): 'absolute' or 'relative'.

    Returns:
        pd.DataFrame: Waterfall data.
    """
    _wfall = inst.wfall_vars
    _is_initial = _wfall.is_initial
    _wtype = _wfall.wfall_type
    sel = data[_is_initial]
    data.loc[sel, _wtype] = initial
    return data
