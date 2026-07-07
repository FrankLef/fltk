from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING, Final
import polars as pl

if TYPE_CHECKING:
    from .main import MungWaterfall  # Only imported when checking types


def get_wfall(inst: MungWaterfall) -> pl.DataFrame:
    _wfall = inst.wfall_vars
    _initial = _wfall.initial
    _is_initial = _wfall.is_initial

    _raw = inst.raw_vars
    _diff_nm = _wfall.diff_nm
    _num_from = _raw.num_from_val
    _total_diff = inst.raw_vars.total_diff

    _keys = list(_raw.groups) + [_raw.ratio_nm]
    _order = list(_raw.groups) + [
        _raw.ratio_nm,
        _raw.period_from,
        _raw.period_to,
        _wfall.diff_nm,
    ]

    wfall = inst.base
    wfall = set_initial(inst, data=wfall, keys=_keys)

    # Remove all other 'num_from_val' not identified as 'initial'.
    wfall = wfall.filter(pl.col(_is_initial) | (pl.col(_diff_nm) != _num_from))

    # Remove rows with 'total_diff' from the data.
    wfall = wfall.filter(pl.col(_diff_nm) != _total_diff)

    wfall = set_wfall_amt(inst, data=wfall)
    wfall = reset_initial(inst, data=wfall, initial=_initial)
    wfall = wfall.sort(by=_order)
    return wfall


def set_initial(
    inst: MungWaterfall, data: pl.DataFrame, keys: list[str]
) -> pl.DataFrame:
    """Set the initial 'num_from_val' to True for the first period and False for all other periods."""
    _raw = inst.raw_vars
    _period = _raw.period_to
    _num_from = _raw.num_from_val

    _wfall = inst.wfall_vars
    _diff_nm = _wfall.diff_nm
    _is_initial = _wfall.is_initial

    sel = (pl.col(_period) == pl.col(_period).min().over(keys)) & (
        pl.col(_diff_nm) == _num_from
    )
    data = data.with_columns(
        pl.when(sel).then(pl.lit(True)).otherwise(pl.lit(False)).alias(_is_initial)
    )
    return data


def set_wfall_amt(inst: MungWaterfall, data: pl.DataFrame) -> pl.DataFrame:
    """Total amount must be set to None (or zero)."""
    TOTAL: Final[str] = "total"
    _wfall = inst.wfall_vars
    _wfall_amt = _wfall.wfall_amt
    _diff_val = _wfall.diff_val
    _wtype = _wfall.wfall_type

    data = data.with_columns(pl.col(_diff_val).alias(_wfall_amt))
    data = data.with_columns(
        pl.when(pl.col(_wtype) == TOTAL)
        .then(None)
        .otherwise(pl.col(_wfall_amt))
        .alias(_wfall_amt)
    )
    return data


def reset_initial(
    inst: MungWaterfall, data: pl.DataFrame, initial: str
) -> pl.DataFrame:
    """Reset initial rows to 'absolute' or 'relative'.

    The first column in a waterfall can be shown as absolute or relative. This
    function reset initial to reflect that choice.

    Args:
        inst (MungWaterfall): MungWaterfall instance.
        data (pl.DataFrame): Waterfall data.
        initial (str): 'absolute' or 'relative'.

    Returns:
        pl.DataFrame: Waterfall data.
    """
    _wfall = inst.wfall_vars
    _is_initial = _wfall.is_initial
    _wtype = _wfall.wfall_type

    data = data.with_columns(
        pl.when(pl.col(_is_initial))
        .then(pl.lit(initial))
        .otherwise(pl.col(_wtype))
        .alias(_wtype)
    )
    return data
