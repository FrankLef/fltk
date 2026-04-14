from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from .main import CalcRatio  # Only imported when checking types


def merge_data(inst: CalcRatio) -> pd.DataFrame:
    raw_data = inst._data
    ratios_data = inst._ratios_df_long
    merged_data = raw_data.merge(
        ratios_data,
        how="inner",
        left_on=inst._data_concept,
        right_on=inst._concept_name,
    )
    if merged_data.empty:
        msg: str = (
            "Merged data is empty. Maybe the concepts don't match with each other."
        )
        raise AssertionError(msg)
    cols = [inst._data_concept, inst._concept_name]
    merged_data.drop(columns=cols, inplace=True)
    pivoted_data = pivot_data(inst, merged_data=merged_data)
    validate_data_keys(inst, data=pivoted_data)
    augmented_data = augment_data(inst, data=pivoted_data)
    final_data = move_cols(inst, data=augmented_data)
    return final_data


def pivot_data(inst: CalcRatio, merged_data: pd.DataFrame) -> pd.DataFrame:
    keys: list[str] = inst._data_group.copy()
    keys.append(inst._concept_ratio)
    pivoted_data = merged_data.pivot(
        index=keys, columns=inst._concept_pos, values=inst._data_value
    )
    # breakpoint()
    pivoted_data.reset_index(inplace=True)
    return pivoted_data


def validate_data_keys(inst: CalcRatio, data: pd.DataFrame) -> None:
    keys: list[str] = inst._data_group.copy()
    keys.append(inst._concept_ratio)
    unique_counts = data[keys].value_counts()
    ndistinct = len(unique_counts)
    if ndistinct != data.shape[0]:
        msg: str = f"Merged data has invalid keys {keys}."
        raise ValueError(msg)
    inst._data_keys = keys


def augment_data(inst: CalcRatio, data: pd.DataFrame) -> pd.DataFrame:
    cols = {inst._concept_num: inst._value_num, inst._concept_den: inst._value_den}
    data.rename(columns=cols, inplace=True)
    augmented_data = data.merge(
        inst._ratios_df,
        how="inner",
        left_on=inst._concept_ratio,
        right_on=inst._concept_ratio,
    )
    return augmented_data


def move_cols(inst: CalcRatio, data: pd.DataFrame) -> pd.DataFrame:
    cols: list[str] = [inst._value_num, inst._value_den]
    new_cols = [col for col in data.columns if col not in cols] + cols
    return data[new_cols]
