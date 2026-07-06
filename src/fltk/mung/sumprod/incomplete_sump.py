from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import polars as pl

if TYPE_CHECKING:
    from .main import MungSumprod  # Only imported when checking types


def get_incomplete_sump(inst: MungSumprod) -> dict[str, pl.DataFrame]:
    sump_df = inst.sump
    _idx_from = inst.sump_vars.idx_from
    _idx_to = inst.sump_vars.idx_to

    _idx = inst.raw_vars.idx  # the index column in the raw data
    _groups = inst.raw_vars.groups

    raw_cols = list(_groups) + [_idx]
    raw_df = inst.raw.select(raw_cols)

    missed_dfs = []
    for idx_to, sump_data in sump_df.group_by(_idx_to):
        for group, data in raw_df.group_by(_groups):
            full_group = tuple(list(group) + [*idx_to])
            missed_df = sump_data.join(
                data, left_on=_idx_from, right_on=_idx, how="anti"
            )
            result = missed_df.with_columns(
                **{col: pl.lit(val) for col, val in zip(_groups, full_group)}
            )
            missed_dfs.append(result)

    incomplete_df = pl.concat(missed_dfs, how="vertical")
    incomplete_df = incomplete_df.sort((_idx_to, _idx_from))
    incomplete_df = incomplete_df.rename({_idx_to: _idx})

    uniq_cols = list(_groups) + [_idx]
    incomplete_uniq_df = incomplete_df.select(uniq_cols).unique()
    # breakpoint()
    return {"incomplete": incomplete_df, "incomplete_uniq": incomplete_uniq_df}
