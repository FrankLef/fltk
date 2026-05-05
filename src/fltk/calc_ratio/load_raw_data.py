from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from .main import CalcRatio  # Only imported when checking types


def load_raw_data(inst: CalcRatio, data: pd.DataFrame) -> pd.DataFrame:
    if inst.ratios.empty:
        msg: str = "You must load the ratio definitions before the data."
        raise ValueError(msg)
    if data.empty:
        raise ValueError("The raw data is empty.")
    validate_data_names(inst, data=data)
    validate_data_keys(inst, data=data)
    all_vars = list(inst.raw_vars.vars)
    reduced_data = data[all_vars]
    return reduced_data


def validate_data_names(inst: CalcRatio, data: pd.DataFrame) -> None:
    data_vars = data.columns.to_list()
    illegal_vars = [var for var in data_vars if var in inst.ratios_vars]
    if illegal_vars:
        msg = f"""
        {illegal_vars} are reserved names.
        Please change these column names.
        """
        raise ValueError(msg)


def validate_data_keys(inst: CalcRatio, data: pd.DataFrame) -> None:
    keys = list(inst.raw_vars.keys)
    unique_counts = data[keys].value_counts()
    ndistinct = len(unique_counts)
    if ndistinct != data.shape[0]:
        msg: str = f"Data has invalid keys {keys}."
        raise ValueError(msg)
