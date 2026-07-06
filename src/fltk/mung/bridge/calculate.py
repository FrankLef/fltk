from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import polars as pl

if TYPE_CHECKING:
    from .main import MungBridge  # Only imported when checking types


def calculate(inst: MungBridge) -> pl.DataFrame:
    _bridge = inst.bridge
    _volume = inst.bridge_vars.volume_diff
    _price = inst.bridge_vars.price_diff
    _mix = inst.bridge_vars.mix_diff
    _total = inst.bridge_vars.total_diff
    _check = inst.bridge_vars.check_diff
    _err = inst.bridge_vars.err
    _den = inst.raw_vars.den_val
    _ratio = inst.raw_vars.ratio_val
    _num = inst.raw_vars.num_val

    _ratio_sfx = inst.add_suffix(_ratio)
    _num_sfx = inst.add_suffix(_num)
    _den_sfx = inst.add_suffix(_den)

    calc_volume_var = (pl.col(_den_sfx[1]) - pl.col(_den)) * pl.col(_ratio)
    _bridge = _bridge.with_columns(calc_volume_var.alias(_volume))

    calc_price_var = (pl.col(_ratio_sfx[1]) - pl.col(_ratio)) * pl.col(_den)
    _bridge = _bridge.with_columns(calc_price_var.alias(_price))

    calc_mix_var = (pl.col(_ratio_sfx[1]) - pl.col(_ratio)) * (
        pl.col(_den_sfx[1]) - pl.col(_den)
    )
    _bridge = _bridge.with_columns(calc_mix_var.alias(_mix))

    calc_total_var = pl.col(_volume) + pl.col(_price) + pl.col(_mix)
    _bridge = _bridge.with_columns(calc_total_var.alias(_total))

    calc_check = pl.col(_num_sfx[1]) - pl.col(_num)
    _bridge = _bridge.with_columns(calc_check.alias(_check))

    calc_err = pl.col(_check) - pl.col(_total)
    _bridge = _bridge.with_columns(calc_err.alias(_err))

    return _bridge
