from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd
from rich.prompt import Confirm

if TYPE_CHECKING:
    from .main import CalcComb  # Only imported when checking types


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
    cols = data.columns.to_list()
    if newvalue_var in cols:
        msg: str = f"'{newvalue_var}' will be replaced with new calculations?"
        if not Confirm.ask(msg, default=True):
            msg = f"Cancelled by user because of '{newvalue_var}'."
            raise ValueError(msg)
    else:
        cols.append(newvalue_var)
    illegal_vars = [var for var in cols if var in inst._comb_vars]
    if illegal_vars:
        msg = f"""
        {illegal_vars} are reserved names.
        Please change these column names.
        """
        raise ValueError(msg)

    invalid_vars = [var for var in inst._data_vars if var not in cols]
    if invalid_vars:
        msg = f"{invalid_vars} are not in data columns."
        raise KeyError(msg)


def validate_data_keys(inst: CalcComb, data: pd.DataFrame) -> None:
    keys = inst._data_keys
    unique_counts = data[keys].value_counts()
    ndistinct = len(unique_counts)
    if ndistinct != data.shape[0]:
        msg: str = f"Data has invalid keys {keys}."
        raise KeyError(msg)
