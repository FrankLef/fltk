import polars as pl
from collections import defaultdict
from typing import Any

from .base import DiczVar as vars

type ItemDict = dict[str, str]
type LineDict = dict[str, ItemDict]
type GroupDict = dict[str, LineDict]


def main(data: pl.DataFrame) -> GroupDict:
    if data.is_empty():
        raise ValueError("The data is empty.")
    audit_columns(data, vars=vars)
    filtered_data = rm_skipped(data)
    nested_dicts = get_nested_dicts(filtered_data)
    return nested_dicts


def audit_columns(data: pl.DataFrame, vars: Any) -> None:
    cols = data.columns

    reserved_nms = [x.value for x in vars]
    missing_nms = [x for x in reserved_nms if x not in cols]
    if missing_nms:
        msg = f"{len(missing_nms)} required columns missing\n{missing_nms}"
        raise KeyError(msg)


def rm_skipped(data: pl.DataFrame) -> pl.DataFrame:
    filtered_data = data.filter(~pl.col(vars.SKIPPED)).drop(vars.SKIPPED)
    return filtered_data


def get_nested_dicts(data: pl.DataFrame) -> GroupDict:
    # Define the nesting keys
    nesting_keys = [vars.GROUP, vars.LINE]

    # Initialize the nested structure
    nested_dict = tree()
    multilevel_dict = nested_dict

    # Loop and dynamically separate keys from remaining columns
    for row in data.iter_rows(named=True):
        # Extract keys and remove them from the row dict
        k1 = row.pop(nesting_keys[0])
        k2 = row.pop(nesting_keys[1])

        # The 'row' dictionary now only contains the remaining unknown columns
        multilevel_dict[k1][k2] = row

    nested_dicts = to_standard_dict(multilevel_dict)
    return nested_dicts


def tree():
    return defaultdict(tree)


def to_standard_dict(mlevel_dict):
    # Convert back to standard dict for clean printing
    if isinstance(mlevel_dict, defaultdict):
        return {k: to_standard_dict(v) for k, v in mlevel_dict.items()}
    return mlevel_dict
