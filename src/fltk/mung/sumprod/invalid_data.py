from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING, Any
import polars as pl
import copy

if TYPE_CHECKING:
    from .main import MungSumprod  # Only imported when checking types


def get_invalid_data(inst: MungSumprod) -> pl.DataFrame:
    groups_df = get_groups(inst)
    invalid_data = find_invalid_items(inst, groups_df=groups_df)
    cleaned_invalid_data = clean_invalid_data(inst, invalid_data=invalid_data)
    return cleaned_invalid_data


def get_groups(inst: MungSumprod) -> pl.DataFrame:
    groups_df = inst.raw.select(inst.raw_vars.groups)
    groups_df = groups_df.unique(maintain_order=True)
    # groups_df = inst.raw[list(inst.raw_vars.groups)]
    # groups_df.drop_duplicates(inplace=True)
    if groups_df.is_empty():
        raise AssertionError("The groups_df is empty.")
    return groups_df


def find_invalid_items(inst: MungSumprod, groups_df: pl.DataFrame) -> pl.DataFrame:
    # MERGE: Final[str] = "_merge"
    raw_data = inst.raw
    idx_from = inst.sump_vars.idx_from
    idx_to = inst.sump_vars.idx_to
    idx_df = inst.sump
    group_vars = inst.raw_vars.groups

    invalid_items = []
    for row in groups_df.iter_rows(named=True):
        # groups_dict = row.to_dict()
        left_df = pl.DataFrame([row])
        matching_df = left_df.join(raw_data, on=group_vars, how="inner")
        merged_df = get_invalid_rows(inst, idx_df=idx_df, data=matching_df)
        invalid_df = merged_df.select([idx_from, idx_to])
        final_df = create_invalid_df(row, invalid_df)
        # left_df = pl.DataFrame([groups_dict])
        # matching_df = pd.merge(left=left_df, right=raw_data, on=group_vars, how="inner")
        # merged_df = get_invalid_rows(inst, idx_df=idx_df, data=matching_df)
        # invalid_df = merged_df.loc[merged_df._merge != "both"]
        # invalid_df = invalid_df[[idx_from, idx_to, MERGE]]
        # final_df = create_invalid_df(groups_dict, invalid_df)
        if not final_df.is_empty():
            invalid_items.append(final_df)

    # i: int = 0
    # for ndx, row in groups_df.iterrows():
    #     groups_dict = row.to_dict()
    #     left_df = pl.DataFrame([groups_dict])
    #     matching_df = pd.merge(left=left_df, right=raw_data, on=group_vars, how="inner")
    #     merged_df = get_invalid_rows(inst, idx_df=idx_df, data=matching_df)
    #     invalid_df = merged_df.loc[merged_df._merge != "both"]
    #     invalid_df = invalid_df[[idx_from, idx_to, MERGE]]
    #     final_df = create_invalid_df(groups_dict, invalid_df)
    #     if not final_df.empty:
    #         invalid_items.append(final_df)
    #     i += 1
    if len(invalid_items):
        invalid_df_all = pl.concat(invalid_items, how="vertical")
        # invalid_df_all.reset_index(drop=True, inplace=True)
    else:
        invalid_df_all = pl.DataFrame()

    is_all_unique = not invalid_df_all.is_duplicated().any()
    # is_all_unique = not invalid_df_all.duplicated().any()
    if (not invalid_df_all.is_empty()) & (not is_all_unique):
        msg: str = "The dataframe of invalid rows must have all unique rows."
        raise AssertionError(msg)
    return invalid_df_all


def get_invalid_rows(
    inst: MungSumprod, idx_df: pl.DataFrame, data: pl.DataFrame
) -> pl.DataFrame:
    left_df = idx_df
    right_df = data
    left_on = inst.sump_vars.idx_from
    right_on = inst.raw_vars.idx
    merged_df = left_df.join(right_df, left_on=left_on, right_on=right_on, how="anti")
    # merged_df = pd.merge(
    #     left=left_df,
    #     right=right_df,
    #     left_on=left_on,
    #     right_on=right_on,
    #     how="left",
    #     indicator=True,
    # )
    if merged_df.is_empty():
        raise AssertionError("The merged_df is empty.")
    return merged_df


def create_invalid_df(
    groups_dict: dict[str, Any], invalid_df: pl.DataFrame
) -> pl.DataFrame:
    # NOTE: Must reset the index to avoid mismatch with NaN in final_df
    # invalid_df.reset_index(drop=True, inplace=True)
    nrows = invalid_df.height
    # nrows = invalid_df.shape[0]
    if nrows:
        the_groups_dicts = [copy.deepcopy(groups_dict) for _ in range(nrows)]
        groups_df = pl.DataFrame(the_groups_dicts)
        # groups_df.reset_index(drop=True, inplace=True)
        final_df = pl.concat([groups_df, invalid_df], how="horizontal")
        # final_df = pd.concat([groups_df, invalid_df], axis=1)
    else:
        final_df = pl.DataFrame()
    return final_df


def clean_invalid_data(inst: MungSumprod, invalid_data: pl.DataFrame) -> pl.DataFrame:
    # MERGE: Final[str] = "_merge"
    left_df = invalid_data
    # invalid_data.drop(columns=MERGE, inplace=True)
    right_df = inst.raw.select(inst.raw_vars.keys)
    # right_df = inst.raw[list(inst.raw_vars.keys)]
    idx_keys = list(inst.raw_vars.groups)
    idx_keys.append(inst.sump_vars.idx_to)
    left_on = idx_keys
    # NOTE: redo data keys to ensure they have same ordering as idx_keys
    data_keys = list(inst.raw_vars.groups)
    data_keys.append(inst.raw_vars.idx)
    right_on = data_keys
    merged_df = left_df.join(
        right_df,
        left_on=left_on,
        right_on=right_on,
        how="inner",
    )
    # merged_df = pd.merge(
    #     left=left_df,
    #     right=right_df,
    #     left_on=left_on,
    #     right_on=right_on,
    #     how="left",
    #     indicator=True,
    # )
    if merged_df.is_empty():
        msg = "The merged_df is empty."
        raise AssertionError(msg)
    # clean_invalid_data = merged_df.loc[merged_df[MERGE] == "both"]
    # clean_invalid_data.drop(columns=[MERGE], inplace=True)
    return merged_df
