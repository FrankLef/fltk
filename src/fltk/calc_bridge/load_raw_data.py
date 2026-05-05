from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from .main import CalcBridge  # Only imported when checking types


def load_raw_data(inst: CalcBridge, data: pd.DataFrame) -> pd.DataFrame:
    if data.empty:
        raise ValueError("The data is empty.")
    validate_data_names(data=data, vars=inst.raw_vars.vars)
    validate_data_keys(data=data, keys=inst.raw_vars.keys)
    return data


def validate_data_names(data: pd.DataFrame, vars: tuple[str, ...]) -> None:
    cols = data.columns.to_list()
    illegal_vars = [var for var in vars if var not in cols]
    if illegal_vars:
        msg = f"{illegal_vars} are not found in the column names."
        raise ValueError(msg)


def validate_data_keys(data: pd.DataFrame, keys: str | tuple[str, ...]) -> None:
    unique_counts = data[list(keys)].value_counts()
    ndistinct = len(unique_counts)
    check = data.shape[0] - ndistinct
    if check:
        msg: str = f"Data has {check} duplicates in the keys."
        raise KeyError(msg)
