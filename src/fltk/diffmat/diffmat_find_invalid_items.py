from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING, Any, NamedTuple, Final
import pandas as pd
import copy

if TYPE_CHECKING:
    from .diffmat import DiffMat  # Only imported when checking types

class InvalidItem(NamedTuple):
    groups: dict[str, Any]
    idx: pd.DataFrame

def get_invalid_items(inst: DiffMat)->Any:
    groups_df = get_groups(inst)
    invalid_items = find_invalid_items(inst, groups_df=groups_df)
    # print(f"\ninvalid_items {invalid_items.shape}:\n", invalid_items)
    return invalid_items

    
def get_groups(inst: DiffMat)->pd.DataFrame:
    groups_df = inst._data[inst._data_group]
    groups_df.drop_duplicates(inplace=True)
    if groups_df.empty:
        msg = "The groups_df is empty."
        raise AssertionError(msg)
    return groups_df

def find_invalid_items(inst: DiffMat, groups_df: pd.DataFrame):    
    MERGED : Final[str] = "both"
    raw_data = inst._data
    idx_from = inst._idx_from
    idx_to = inst._idx_to
    idx_df = inst._idx_df
    group_vars = inst._data_group
    invalid_items = []
    i = 0
    for ndx, row in groups_df.iterrows():
        groups_dict = row.to_dict()
        left_df=pd.DataFrame([groups_dict])
        matching_df = pd.merge(left=left_df, right=raw_data, on=group_vars, how='inner')
        # print(f"\nmatching_df {i}")
        # matching_df.info()
        merged_df = get_invalid_rows(inst, idx_df=idx_df, data=matching_df)
        # print(f"\nmerged_df {i}")
        # merged_df.info()
        invalid_df = merged_df.loc[merged_df._merge != MERGED]
        # print(f"\ninvalid_df {i}")
        # invalid_df.info()
        invalid_df = invalid_df[[idx_from, idx_to]]
        # print("\ninvalid_df:\n", invalid_df.head())
        i += 1
        final_df = create_invalid_df(groups_dict, invalid_df)
        if not final_df.empty:
            invalid_items.append(final_df)
        # invalid_item = InvalidItem(groups=groups_dict, idx=invalid_df)
        # invalid_items.append(invalid_item)
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

def get_invalid_rows(inst:DiffMat, idx_df: pd.Dataframe, data: pd.DataFrame):
        left_df = idx_df
        right_df = data
        left_on = inst._idx_from
        right_on = "period"
        merged_df = pd.merge(left_df, right_df, left_on=left_on, right_on=right_on, how='left', indicator=True)
        # print("\nmerged_df:\n", merged_df.head())
        if merged_df.empty:
            msg = "The merged_df is empty."
            raise AssertionError(msg)
        return merged_df

def create_invalid_df(groups_dict: dict[str,Any], invalid_df: pd.DataFrame)->pd.Dataframe:
    # NOTE: Must reset the index to avoid mismatch with NaN in final_df
    invalid_df.reset_index(drop=True, inplace=True)
    nrows = invalid_df.shape[0]
    final_df = pd.DataFrame()
    if nrows:
        the_groups_dicts = [copy.deepcopy(groups_dict) for _ in range(nrows)]
        # print("\nthe_groups_dict\n", the_groups_dicts)
        groups_df = pd.DataFrame(the_groups_dicts)
        groups_df.reset_index(drop=True, inplace=True)
        # print(f"\ngroups_df, {groups_df.shape}\n", groups_df)
        # print(f"\ninvalid_df, {invalid_df.shape}\n", invalid_df)
        final_df = pd.concat([groups_df, invalid_df], axis=1)
        # print(f"\nfinal_df, {final_df.shape}\n", final_df)
    return final_df