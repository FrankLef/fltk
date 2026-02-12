from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING, Iterable
import pandas as pd

if TYPE_CHECKING:
    from .diffmat import DiffMat  # Only imported when checking types


def load_data(
    inst: DiffMat,
    data: pd.DataFrame,
    idx_var: str,
    value_var: str,
    group_vars: Iterable[str],
) -> None:
    if inst._idx_df.empty:
        msg: str = "You must load the matrix before the data."
        raise ValueError(msg)
    validate_data_names(inst, data=data)
    inst._data_idx = idx_var
    inst._data_value = value_var
    inst._data_group = group_vars
    validate_data_keys(inst, data=data, idx_var=idx_var, group_vars=group_vars)
    inst._data = data


def validate_data_names(inst: DiffMat, data: pd.DataFrame) -> None:
    reserved_vars = inst._reserved_vars
    data_vars = data.columns.to_list()
    illegal_vars = [var for var in data_vars if var in reserved_vars]
    if illegal_vars:
        msg: str = f"""
        {illegal_vars} are reserved names.
        Please change these column names.
        """
        raise ValueError(msg)


def validate_data_keys(
    inst: DiffMat, data: pd.DataFrame, idx_var: str, group_vars: Iterable[str]
) -> None:
    keys: list[str]= list(group_vars)
    keys.append(idx_var)
    unique_counts = data[keys].value_counts()
    ndistinct = len(unique_counts)
    if ndistinct != data.shape[0]:
        msg: str = f"Data has invalid keys {keys}."
        raise ValueError(msg)
    inst._data_keys = keys
