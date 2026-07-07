from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import polars as pl

if TYPE_CHECKING:
    from .main import MungWaterfall  # Only imported when checking types


def get_base(inst: MungWaterfall) -> pl.DataFrame:
    if inst.raw.is_empty():
        raise ValueError("Raw data is empty.")
    wfall_types = get_wfall_types(inst)
    wfall_factors = list(wfall_types.keys())
    data_long = melt_raw(inst, factors=wfall_factors)
    base_df = add_wfall_type(inst, data_long=data_long, wfall_types=wfall_types)
    base_df = base_df.with_columns(pl.lit(False).alias(inst.wfall_vars.is_initial))

    return base_df


def melt_raw(inst: MungWaterfall, factors: list[str]) -> pl.DataFrame:
    _keys = inst.raw_vars.keys
    _factors = inst.raw_vars.factors
    _vars = inst.raw_vars.vars
    _diff_nm = inst.wfall_vars.diff_nm
    _diff_val = inst.wfall_vars.diff_val

    data_wide = inst.raw.select(_vars)

    data_long = data_wide.unpivot(
        index=_keys, on=_factors, variable_name=_diff_nm, value_name=_diff_val
    )
    data_long = data_long.with_columns(pl.col(_diff_nm).cast(pl.Enum(_factors)))
    data_long = data_long.sort(by=list(_keys))
    return data_long


def get_wfall_types(inst: MungWaterfall) -> dict[str, str]:
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
    inst: MungWaterfall, data_long: pl.DataFrame, wfall_types: dict[str, str]
) -> pl.DataFrame:
    _diff_nm = inst.wfall_vars.diff_nm
    _wfall_type = inst.wfall_vars.wfall_type

    data_long = data_long.with_columns(
        pl.col(_diff_nm).cast(pl.String).alias(_wfall_type)
    )
    data_long = data_long.with_columns(
        pl.col(_wfall_type).replace_strict(wfall_types, default=None)
    )

    null_nb = data_long[_wfall_type].null_count()
    if null_nb:
        msg: str = f"{null_nb} rows with empty waterfall type."
        raise AssertionError(msg)

    types = list(wfall_types.values())
    err_df = data_long.filter(~pl.col(_wfall_type).is_in(types))
    if err_df.height:
        msg = f"{err_df.height} rows with invalid waterfall type."
        raise AssertionError(msg)

    return data_long
