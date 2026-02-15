from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING, Iterable
import pandas as pd
from rich.prompt import Confirm

if TYPE_CHECKING:
    from .diffmat import DiffMat  # Only imported when checking types


def load_data(
    inst: DiffMat,
    data: pd.DataFrame,
    idx_var: str,
    value_var: str,
    group_vars: Iterable[str],
    newvalue_var: str,
) -> pd.DataFrame:
    if inst._idx_df.empty:
        msg: str = "You must load the matrix before the data."
        raise ValueError(msg)
    inst._data_idx = idx_var  # variable used by idx, usually the period
    inst._data_value = value_var  # variable used to calculate
    inst._data_group = group_vars  # variable representing a composite key
    inst._data_newvalue = newvalue_var  # new variable for calculated values
    validate_data_names(inst, data=data, newvalue_var=newvalue_var)
    validate_data_keys(inst, data=data, idx_var=idx_var, group_vars=group_vars)
    return data


def validate_data_names(inst: DiffMat, data: pd.DataFrame, newvalue_var: str) -> None:
    reserved_vars = inst._reserved_vars
    data_vars = data.columns.to_list()
    if newvalue_var in data_vars:
        msg: str = f"'{newvalue_var}' will be replaced with new calculations?"
        if not Confirm.ask(msg, default=True):
            msg = f"Cancelled by user because of '{newvalue_var}'."
            raise ValueError(msg)
    else:
        data_vars.append(newvalue_var)
    illegal_vars = [var for var in data_vars if var in reserved_vars]
    if illegal_vars:
        msg = f"""
        {illegal_vars} are reserved names.
        Please change these column names.
        """
        raise ValueError(msg)


def validate_data_keys(
    inst: DiffMat, data: pd.DataFrame, idx_var: str, group_vars: Iterable[str]
) -> None:
    keys: list[str] = list(group_vars)
    keys.append(idx_var)
    unique_counts = data[keys].value_counts()
    ndistinct = len(unique_counts)
    if ndistinct != data.shape[0]:
        msg: str = f"Data has invalid keys {keys}."
        raise ValueError(msg)
    inst._data_keys = keys
