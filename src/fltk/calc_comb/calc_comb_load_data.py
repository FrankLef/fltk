from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd
from rich.prompt import Confirm

if TYPE_CHECKING:
    from .calc_comb import CalcComb  # Only imported when checking types


def load_data(
    inst: CalcComb,
    data: pd.DataFrame,
    idx_var: str,
    value_var: str,
    group_vars: list[str],
    newvalue_var: str,
) -> pd.DataFrame:
    if inst._combs_df.empty:
        msg: str = "You must load the matrix before the data."
        raise ValueError(msg)
    inst._data_idx = idx_var
    inst._data_value = value_var
    inst._data_group = group_vars
    inst._data_newvalue = newvalue_var
    validate_data_names(inst, data=data, newvalue_var=newvalue_var)
    validate_data_keys(inst, data=data)
    return data


def validate_data_names(inst: CalcComb, data: pd.DataFrame, newvalue_var: str) -> None:
    data_vars = data.columns.to_list()
    if newvalue_var in data_vars:
        msg: str = f"'{newvalue_var}' will be replaced with new calculations?"
        if not Confirm.ask(msg, default=True):
            msg = f"Cancelled by user because of '{newvalue_var}'."
            raise ValueError(msg)
    else:
        data_vars.append(newvalue_var)
    illegal_vars = [var for var in data_vars if var in inst._comb_vars]
    if illegal_vars:
        msg = f"""
        {illegal_vars} are reserved names.
        Please change these column names.
        """
        raise ValueError(msg)
    args_vars = inst._data_group.copy()
    args_vars.append(inst._data_idx)
    args_vars.append(inst._data_value)
    invalid_vars = [var for var in args_vars if var not in data_vars]
    if invalid_vars:
        msg = f"{invalid_vars} are not in columns of data."
        raise KeyError(msg)


def validate_data_keys(inst: CalcComb, data: pd.DataFrame) -> None:
    keys: list[str] = list(inst._data_group)
    keys.append(inst._data_idx)
    unique_counts = data[keys].value_counts()
    ndistinct = len(unique_counts)
    if ndistinct != data.shape[0]:
        msg: str = f"Data has invalid keys {keys}."
        raise ValueError(msg)
    inst._data_keys = keys
