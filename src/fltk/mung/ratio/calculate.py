from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import polars as pl

if TYPE_CHECKING:
    from .main import MungRatio  # Only imported when checking types


def calculate(inst: MungRatio) -> pl.DataFrame:
    data = inst.merged

    calc_ratio = pl.col(inst.ratios_vars.value_num) / pl.col(inst.ratios_vars.value_den)
    data = data.with_columns(calc_ratio.alias(inst.ratios_vars.value_ratio))
    return data
