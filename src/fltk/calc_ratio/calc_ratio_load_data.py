from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING, Iterable
import pandas as pd

if TYPE_CHECKING:
    from .calc_ratio import CalcRatio  # Only imported when checking types


def load_data(
    inst: CalcRatio,
    data: pd.DataFrame,
    concept_var: str,
    value_var: str,
    group_vars: Iterable[str],
) -> pd.DataFrame:
    if inst._ratios_df.empty:
        msg: str = "You must load the ratio definitions before the data."
        raise ValueError(msg)
    inst._data_concept = concept_var
    inst._data_value = value_var
    inst._data_group = group_vars
    validate_data_names(inst, data=data)
    validate_data_keys(inst, data=data)
    return data


def validate_data_names(inst: CalcRatio, data: pd.DataFrame) -> None:
    reserved_vars = inst._reserved_vars
    data_vars = data.columns.to_list()
    illegal_vars = [var for var in data_vars if var in reserved_vars]
    if illegal_vars:
        msg = f"""
        {illegal_vars} are reserved names.
        Please change these column names.
        """
        raise ValueError(msg)


def validate_data_keys(inst: CalcRatio, data: pd.DataFrame) -> None:
    keys: list[str] = list(inst._data_group)
    keys.append(inst._data_concept)
    unique_counts = data[keys].value_counts()
    ndistinct = len(unique_counts)
    if ndistinct != data.shape[0]:
        msg: str = f"Data has invalid keys {keys}."
        raise ValueError(msg)
    inst._data_keys = keys
