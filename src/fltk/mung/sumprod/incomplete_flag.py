from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING, Final
import polars as pl

if TYPE_CHECKING:
    from .main import MungSumprod  # Only imported when checking types


def flag_incomplete(inst: MungSumprod) -> pl.DataFrame:
    FLAG_COL: Final[str] = "incomplete_sump"
    calc_df = inst.calc
    _idx = inst.raw_vars.idx  # the index column in the raw data
    _groups = inst.raw_vars.groups

    incomplete_uniq_df = inst.incomplete_uniq

    _join_cols = list(_groups) + [_idx]

    augmented_calc = calc_df.join(
        incomplete_uniq_df.select(_join_cols).with_columns(
            pl.lit(True).alias(FLAG_COL)
        ),
        on=_join_cols,
        how="left",
    ).with_columns(pl.col(FLAG_COL).fill_null(False))

    if calc_df.height != augmented_calc.height:
        msg: str = f"Calc has {calc_df.height} whereas augmented_calc has {augmented_calc.height}. Weird!"
        raise AssertionError(msg)

    return augmented_calc
