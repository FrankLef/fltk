import polars as pl

from .vars import RawVars, SumprodVars


def calculate(
    data: pl.DataFrame,
    sumprod: pl.DataFrame,
    raw_vars: RawVars,
    sump_vars: SumprodVars,
    missing_to_zero: bool,
) -> pl.DataFrame:
    _idx_from = sump_vars.idx_from
    _idx_to = sump_vars.idx_to
    _coef = sump_vars.sump_coef

    _idx = raw_vars.idx
    _groups = raw_vars.groups
    _value = raw_vars.value
    _newvalue = raw_vars.newvalue

    dfs = []
    for _, sump_df in sumprod.group_by(_idx_to):
        for group_vals, raw_df in data.group_by(_groups):
            merged_df = sump_df.join(
                raw_df, left_on=_idx_from, right_on=_idx, how="left"
            )
            # add groups to see which one had missing data
            cols = {col: pl.lit(val) for col, val in zip(_groups, group_vals)}
            merged_df = (
                merged_df.with_columns(**cols)
                .with_columns((pl.col(_coef) * pl.col(_value)).alias(_newvalue))
                .with_columns(
                    pl.when(missing_to_zero)
                    .then(pl.col(_newvalue).fill_null(0))
                    .otherwise(pl.col(_newvalue))
                )
            )

            dfs.append(merged_df)

    all_df = pl.concat(dfs, how="vertical")

    all_groups = list(_groups) + [_idx_to]
    final_df = (
        all_df.group_by(all_groups)
        .agg(
            pl.when(pl.col(_newvalue).has_nulls())
            .then(None)
            .otherwise(pl.col(_newvalue).sum())
            .alias(_newvalue)
        )
        .sort(all_groups)
        .rename({_idx_to: _idx})
    )

    return final_df
