from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING, Final
import pandas as pd

if TYPE_CHECKING:
    from .main import CalcWaterfall  # Only imported when checking types


def get_wfall(inst: CalcWaterfall) -> pd.DataFrame:
    wfall = inst.base.copy()
    _keys = list(inst.raw_vars.keys)

    for _, group in wfall.groupby(_keys):
        wfall = set_initial(inst, data=wfall, group=group)
    wfall = rm_total_diff(inst, data=wfall)
    return wfall


def set_initial(
    inst: CalcWaterfall, data: pd.DataFrame, group: pd.DataFrame
) -> pd.DataFrame:
    VAL_INITIAL: Final[str] = "initial"
    _raw = inst.raw_vars
    _period = _raw.period_to
    _num_from = _raw.num_from_val
    _wfall = inst.wfall_vars
    _diff_nm = _wfall.diff_nm
    _wtype = _wfall.wfall_type
    period_sel = group[_period] == group[_period].min()
    num_sel = group[_diff_nm] == _num_from
    sel = period_sel & num_sel
    group_sel = group[sel]
    data.loc[group_sel.index, _wtype] = VAL_INITIAL
    return data


def rm_total_diff(inst: CalcWaterfall, data: pd.DataFrame) -> pd.DataFrame:
    _diff_nm = inst.wfall_vars.diff_nm
    _total_diff = inst.raw_vars.total_diff
    sel = data[_diff_nm] != _total_diff
    data = data.loc[sel]
    return data
