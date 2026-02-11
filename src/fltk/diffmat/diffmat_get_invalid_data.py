from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING, Any, Final
import pandas as pd
import copy

if TYPE_CHECKING:
    from .diffmat import DiffMat  # Only imported when checking types


def get_invalid_data(inst: DiffMat) -> pd.DataFrame:
    groups_df = get_groups(inst)
    invalid_data = find_invalid_items(inst, groups_df=groups_df)
    # print(f"\ninvalid_data {invalid_data.shape}:\n", invalid_data)
    cleaned_invalid_data = clean_invalid_data(inst, invalid_data=invalid_data)
    # print("\nclean_invalid_data:\n", clean_invalid_data)
    return cleaned_invalid_data


def get_groups(inst: DiffMat) -> pd.DataFrame:
    groups_df = inst._data[inst._data_group]
    groups_df.drop_duplicates(inplace=True)
    if groups_df.empty:
        msg = "The groups_df is empty."
        raise AssertionError(msg)
    return groups_df


def find_invalid_items(inst: DiffMat, groups_df: pd.DataFrame) -> pd.DataFrame:
    MERGE: Final[str] = "_merge"
    MERGE_BOTH: Final[str] = "both"
    HOW_INNER: Final[str] = "inner"
    raw_data = inst._data
    idx_from = inst._idx_from
    idx_to = inst._idx_to
    idx_df = inst._idx_df
    group_vars = inst._data_group
    invalid_items = []
    i = 0
    for ndx, row in groups_df.iterrows():
        groups_dict = row.to_dict()
        left_df = pd.DataFrame([groups_dict])
        matching_df = pd.merge(left=left_df, right=raw_data, on=group_vars, how=HOW_INNER)
        merged_df = get_invalid_rows(inst, idx_df=idx_df, data=matching_df)
        invalid_df = merged_df.loc[merged_df._merge != MERGE_BOTH]
        invalid_df = invalid_df[[idx_from, idx_to, MERGE]]
        final_df = create_invalid_df(groups_dict, invalid_df)
        if not final_df.empty:
            invalid_items.append(final_df)
        i += 1
    if len(invalid_items):
        invalid_df_all = pd.concat(invalid_items)
        invalid_df_all.reset_index(drop=True, inplace=True)
    else:
        invalid_df_all = pd.DataFrame()
    is_all_unique = not invalid_df_all.duplicated().any()
    if (not invalid_df_all.empty) & (not is_all_unique):
        msg: str = "The dataframe of invalid rows must have all unique rows."
        raise AssertionError(msg)
    return invalid_df_all


def get_invalid_rows(
    inst: DiffMat, idx_df: pd.Dataframe, data: pd.DataFrame
) -> pd.DataFrame:
    HOW_LEFT: Final[str] = "left"
    left_df = idx_df
    right_df = data
    left_on = inst._idx_from
    right_on = inst._data_idx
    merged_df = pd.merge(
        left_df,
        right_df,
        left_on=left_on,
        right_on=right_on,
        how=HOW_LEFT,
        indicator=True,
    )
    if merged_df.empty:
        msg = "The merged_df is empty."
        raise AssertionError(msg)
    return merged_df


def create_invalid_df(
    groups_dict: dict[str, Any], invalid_df: pd.DataFrame
) -> pd.DataFrame:
    # NOTE: Must reset the index to avoid mismatch with NaN in final_df
    invalid_df.reset_index(drop=True, inplace=True)
    nrows = invalid_df.shape[0]
    if nrows:
        the_groups_dicts = [copy.deepcopy(groups_dict) for _ in range(nrows)]
        groups_df = pd.DataFrame(the_groups_dicts)
        groups_df.reset_index(drop=True, inplace=True)
        final_df = pd.concat([groups_df, invalid_df], axis=1)
    else:
        final_df = pd.DataFrame()
    return final_df

def clean_invalid_data(inst: DiffMat, invalid_data: pd.DataFrame)-> pd.DataFrame:
    MERGE: Final[str] = "_merge"
    HOW_LEFT: Final[str] = "left"
    MERGE_BOTH: Final[str] = "both"
    left_df = invalid_data
    invalid_data.drop(columns=MERGE, inplace=True)
    right_df = inst._data[inst._data_keys]
    idx_keys = list(inst._data_group)
    idx_keys.append(inst._idx_to)
    left_on = idx_keys
    # NOTE: redo data keys to ensure they have same ordering as idx_keys
    data_keys = list(inst._data_group)
    data_keys.append(inst._data_idx)
    right_on = data_keys
    merged_df = pd.merge(
        left_df,
        right_df,
        left_on=left_on,
        right_on=right_on,
        how=HOW_LEFT,
        indicator=True,
    )
    if merged_df.empty:
        msg = "The merged_df is empty."
        raise AssertionError(msg)
    # print("\nclean_invalid_data, merged_df:\n", merged_df)
    clean_invalid_data = merged_df.loc[merged_df[MERGE]==MERGE_BOTH]
    clean_invalid_data.drop(columns=[MERGE], inplace=True)
    # print("\nclean_invalid_data:\n", clean_invalid_data)
    return clean_invalid_data