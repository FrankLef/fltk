from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd
from pandas.api.types import CategoricalDtype

if TYPE_CHECKING:
    from .main import CalcBridge  # Only imported when checking types


def get_waterfall(inst: CalcBridge) -> pd.DataFrame:
    if inst.bridge.empty:
        raise ValueError("Bridge data is empty.")
    wfall_types = get_wfall_types(inst)
    wfall_factors = list(wfall_types.keys())
    data_long = melt_waterfall(inst, factors=wfall_factors)
    wfall_df = add_wfall_type(inst, data_long=data_long, wfall_types=wfall_types)

    return wfall_df


def melt_waterfall(inst: CalcBridge, factors: list[str]) -> pd.DataFrame:
    _groups = inst.raw_vars.groups
    _concept_ratio = inst.raw_vars.ratio_nm
    _periods = inst.periods_vars.vars
    _diff_nm = inst.wfall_vars.diff_nm
    _diff_val = inst.wfall_vars.diff_val

    keys: list[str] = list(_groups) + [_concept_ratio] + list(_periods)

    data_wide = inst.bridge.copy()
    cols = keys + list(factors)
    data_wide = data_wide[cols]

    data_long = data_wide.melt(
        id_vars=keys, value_vars=factors, var_name=_diff_nm, value_name=_diff_val
    )
    cat_dtype = CategoricalDtype(categories=factors, ordered=True)
    data_long[_diff_nm] = data_long[_diff_nm].astype(cat_dtype)
    return data_long


def get_wfall_types(inst: CalcBridge) -> dict[str, str]:
    _concept_num_nms = inst.add_suffix(inst.raw_vars.num_val)
    vars = inst.bridge_vars
    wfall_types: dict[str, str] = {
        _concept_num_nms[0]: "absolute",
        vars.price_diff: "relative",
        vars.volume_diff: "relative",
        vars.mix_diff: "relative",
        vars.total_diff: "relative",
        _concept_num_nms[1]: "total",
    }
    return wfall_types


def add_wfall_type(
    inst: CalcBridge, data_long: pd.DataFrame, wfall_types: dict[str, str]
) -> pd.DataFrame:
    _diff_nm = inst.wfall_vars.diff_nm
    _wfall_type = inst.wfall_vars.wfall_type
    data_long[_wfall_type] = data_long[_diff_nm].astype(str)
    data_long[_wfall_type] = data_long[_wfall_type].replace(wfall_types)

    types = list(wfall_types.values())
    err_df = data_long[~data_long[_wfall_type].isin(types)]
    if not err_df.empty:
        msg: str = f"{err_df.shape[0]} rows in waterfall with invalid wfall type."
        raise AssertionError(msg)
    return data_long
