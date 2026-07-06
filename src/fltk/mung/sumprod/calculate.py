from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import polars as pl

if TYPE_CHECKING:
    from .main import MungSumprod  # Only imported when checking types


def calculate(inst: MungSumprod) -> pl.DataFrame:
    raw_df = inst.raw
    _idx = inst.raw_vars.idx  # the index column in the raw data
    _newvalue = inst.raw_vars.newvalue
    _groups = inst.raw_vars.groups

    sump_df = inst.sump
    _idx_from = inst.sump_vars.idx_from
    _idx_to = inst.sump_vars.idx_to
    _sump_coef = inst.sump_vars.sump_coef

    merged_df = raw_df.join(sump_df, left_on=_idx, right_on=_idx_from, how="inner")

    # df = pd.merge(
    #     left=inst.valid,
    #     right=inst.sump,
    #     left_on=inst.raw_vars.idx,
    #     right_on=inst.sump_vars.idx_from,
    # )
    calc_newval = pl.col(_sump_coef) * pl.col(inst.raw_vars.value)
    merged_df = merged_df.with_columns(calc_newval.alias(_newvalue))

    calc_groups = list(_groups) + [_idx_to]
    calc_data = merged_df.group_by(calc_groups).agg(pl.col(_newvalue).sum())
    calc_data = calc_data.sort(calc_groups)
    calc_data = calc_data.rename({_idx_to: _idx})
    # sumkeys = list(inst.raw_vars.groups)
    # sumkeys.append(inst.sump_vars.idx_to)
    # calc_data = df.groupby(by=sumkeys, as_index=False)[inst.raw_vars.newvalue].sum()
    return calc_data
