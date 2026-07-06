from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import polars as pl

if TYPE_CHECKING:
    from .main import MungSumprod  # Only imported when checking types


def flag_incomplete(inst: MungSumprod) -> pl.DataFrame:
    calc_df = inst.calc
    _idx = inst.raw_vars.idx  # the index column in the raw data
    _groups = inst.raw_vars.groups

    incomplete_uniq_df = inst.incomplete_uniq

    flag_col = "incomplete_sump"

    _join_cols = list(_groups) + [_idx]
    breakpoint()
    augmented_calc = calc_df.join(
        incomplete_uniq_df.select(_join_cols).with_columns(
            pl.lit(True).alias(flag_col)
        ),
        on=_join_cols,
        how="left",
    ).with_columns(pl.col(flag_col).fill_null(False))

    return augmented_calc
