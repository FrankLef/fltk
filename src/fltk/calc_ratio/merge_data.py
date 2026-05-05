from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from .main import CalcRatio  # Only imported when checking types


def merge_data(inst: CalcRatio) -> pd.DataFrame:
    raw_data = inst.raw
    ratios_data = inst.ratios_long
    _data_concept = inst.raw_vars.concept
    _concept_name = inst.ratios_vars.concept_name
    merged_data = raw_data.merge(
        ratios_data,
        how="inner",
        left_on=_data_concept,
        right_on=_concept_name,
    )
    if merged_data.empty:
        msg: str = (
            "Merged data is empty. Maybe the concepts don't match with each other."
        )
        raise AssertionError(msg)
    cols = [_data_concept, _concept_name]
    merged_data.drop(columns=cols, inplace=True)
    pivoted_data = pivot_data(inst, merged_data=merged_data)
    validate_data_keys(inst, data=pivoted_data)
    augmented_data = augment_data(inst, data=pivoted_data)
    final_data = move_cols(inst, data=augmented_data)
    return final_data


def pivot_data(inst: CalcRatio, merged_data: pd.DataFrame) -> pd.DataFrame:
    keys: list[str] = list(inst.raw_vars.groups) + [inst.ratios_vars.concept_ratio]
    _concept_pos = inst.ratios_vars.concept_pos
    _data_value = inst.raw_vars.value
    pivoted_data = merged_data.pivot(
        index=keys, columns=_concept_pos, values=_data_value
    )
    pivoted_data.reset_index(inplace=True)
    return pivoted_data


def validate_data_keys(inst: CalcRatio, data: pd.DataFrame) -> None:
    keys: list[str] = list(inst.raw_vars.groups) + [inst.ratios_vars.concept_ratio]
    unique_counts = data[keys].value_counts()
    ndistinct = len(unique_counts)
    if ndistinct != data.shape[0]:
        msg: str = f"Merged data has invalid keys {keys}."
        raise ValueError(msg)


def augment_data(inst: CalcRatio, data: pd.DataFrame) -> pd.DataFrame:
    cols = {
        inst.ratios_vars.concept_num: inst.ratios_vars.value_num,
        inst.ratios_vars.concept_den: inst.ratios_vars.value_den,
    }
    data.rename(columns=cols, inplace=True)
    _concept_ratio = inst.ratios_vars.concept_ratio
    augmented_data = data.merge(
        inst.ratios,
        how="inner",
        left_on=_concept_ratio,
        right_on=_concept_ratio,
    )
    return augmented_data


def move_cols(inst: CalcRatio, data: pd.DataFrame) -> pd.DataFrame:
    cols: list[str] = [inst.ratios_vars.value_num, inst.ratios_vars.value_den]
    new_cols = [col for col in data.columns if col not in cols] + cols
    return data[new_cols]
