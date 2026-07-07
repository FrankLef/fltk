import polars as pl
from .vars import RawVars


def flag_incomplete(
    calc: pl.DataFrame,
    incomplete_uniq: pl.DataFrame,
    raw_vars: RawVars,
    flag_col: str = "incomplete_sump",
) -> pl.DataFrame:
    _idx = raw_vars.idx  # the index column in the raw data
    _groups = raw_vars.groups

    _join_cols = list(_groups) + [_idx]

    augmented_calc = calc.join(
        incomplete_uniq.select(_join_cols).with_columns(pl.lit(True).alias(flag_col)),
        on=_join_cols,
        how="left",
    ).with_columns(pl.col(flag_col).fill_null(False))

    if calc.height != augmented_calc.height:
        msg: str = f"Calc has {calc.height} whereas augmented_calc has {augmented_calc.height}. Weird!"
        raise AssertionError(msg)

    return augmented_calc
