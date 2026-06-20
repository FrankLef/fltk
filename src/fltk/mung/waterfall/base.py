from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd
from pandas.api.types import CategoricalDtype

if TYPE_CHECKING:
    from .main import CalcWaterfall  # Only imported when checking types


def get_base(inst: CalcWaterfall) -> pd.DataFrame:
    if inst.raw.empty:
        raise ValueError("Raw data is empty.")
    wfall_types = get_wfall_types(inst)
    wfall_factors = list(wfall_types.keys())
    data_long = melt_raw(inst, factors=wfall_factors)
    base_df = add_wfall_type(inst, data_long=data_long, wfall_types=wfall_types)

    base_df[inst.wfall_vars.is_initial] = False

    return base_df


def melt_raw(inst: CalcWaterfall, factors: list[str]) -> pd.DataFrame:
    _keys = inst.raw_vars.keys
    _factors = inst.raw_vars.factors
    _vars = inst.raw_vars.vars
    _diff_nm = inst.wfall_vars.diff_nm
    _diff_val = inst.wfall_vars.diff_val

    data_wide = inst.raw.copy()
    data_wide = data_wide[list(_vars)]

    data_long = data_wide.melt(
        id_vars=_keys, value_vars=_factors, var_name=_diff_nm, value_name=_diff_val
    )
    cat_dtype = CategoricalDtype(categories=_factors, ordered=True)
    data_long[_diff_nm] = data_long[_diff_nm].astype(cat_dtype)
    data_long = data_long.sort_values(by=list(_keys))
    return data_long


def get_wfall_types(inst: CalcWaterfall) -> dict[str, str]:
    _vars = inst.raw_vars
    wfall_types: dict[str, str] = {
        _vars.num_from_val: "absolute",
        _vars.price_diff: "relative",
        _vars.volume_diff: "relative",
        _vars.mix_diff: "relative",
        _vars.total_diff: "relative",
        _vars.num_to_val: "total",
    }
    err_set = set(_vars.factors).symmetric_difference(set(wfall_types.keys()))
    err_nb = len(err_set)
    if err_nb:
        msg: str = f"There are {err_nb} discrepancies in wfall_types."
        raise KeyError(msg)
    return wfall_types


def add_wfall_type(
    inst: CalcWaterfall, data_long: pd.DataFrame, wfall_types: dict[str, str]
) -> pd.DataFrame:
    _diff_nm = inst.wfall_vars.diff_nm
    _wfall_type = inst.wfall_vars.wfall_type
    data_long[_wfall_type] = data_long[_diff_nm].astype(str)
    data_long[_wfall_type] = data_long[_wfall_type].replace(wfall_types)

    err_df = data_long[data_long[_wfall_type].isna()]
    err_nb = err_df.shape[0]
    if err_nb:
        msg: str = f"{err_nb} rows with empty waterfall type."
        raise AssertionError(msg)

    types = list(wfall_types.values())
    err_df = data_long[~data_long[_wfall_type].isin(types)]
    err_nb = err_df.shape[0]
    if err_nb:
        msg = f"{err_nb} rows with invalid waterfall type."
        raise AssertionError(msg)

    return data_long
