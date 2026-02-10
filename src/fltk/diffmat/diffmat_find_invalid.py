from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from .diffmat import DiffMat  # Only imported when checking types

def get_invalid_items(inst: DiffMat)->Any:
    groups_df = get_groups_data(inst)
    invalid_items = find_invalid_items(inst, groups_df=groups_df)
    print("\ninvalid_items:\n", invalid_items)
    return invalid_items

    
def get_groups_data(inst: DiffMat)->pd.DataFrame:
    groups_df = inst._data[inst._data_group]
    groups_df.drop_duplicates(inplace=True)
    if groups_df.empty:
        msg = "The groups_df is empty."
        raise AssertionError(msg)
    return groups_df

def find_invalid_items(inst: DiffMat, groups_df: pd.DataFrame):    
    raw_data = inst._data
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
        invalid_df = merged_df.loc[merged_df._merge != "both"]
        # print(f"\ninvalid_df {i}")
        # invalid_df.info()
        invalid_df = invalid_df[["idx_from", "idx"]]
        # print("\ninvalid_df:\n", invalid_df.head())
        i += 1
        invalid_items.append([groups_dict, invalid_df])
    return invalid_items

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
