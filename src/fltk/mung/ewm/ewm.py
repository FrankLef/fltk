from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import polars as pl

if TYPE_CHECKING:
    from .main import MungEwm  # Only imported when checking types


def get_ewm(inst: MungEwm) -> pl.DataFrame:
    _ewm = inst.ewm_vars
    _raw = inst.raw_vars

    sort_vars = list(_raw.groups) + [_raw.period]
    data_ewm = inst.raw.sort(by=sort_vars, descending=False)

    for value in _raw.values:
        ewm_nm = value + "_" + _ewm.suffix
        data_ewm = data_ewm.with_columns(
            pl.col(value)
            .ewm_mean(span=_ewm.span, adjust=True)
            .over(list(_raw.groups))
            .alias(ewm_nm)
        )

    return data_ewm
