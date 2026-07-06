from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import polars as pl

if TYPE_CHECKING:
    from .main import MungRatio  # Only imported when checking types


def merge_data(inst: MungRatio) -> pl.DataFrame:
    raw_data = inst.raw
    ratios_data = inst.ratios_long
    _data_concept = inst.raw_vars.concept
    _concept_name = inst.ratios_vars.concept_nm
    merged_data = raw_data.join(
        ratios_data,
        how="inner",
        left_on=_data_concept,
        right_on=_concept_name,
    )
    if merged_data.is_empty():
        raise AssertionError("Merged data is empty.")
    pivoted_data = pivot_data(inst, merged_data=merged_data)
    augmented_data = augment_data(inst, data=pivoted_data)
    return augmented_data


def pivot_data(inst: MungRatio, merged_data: pl.DataFrame) -> pl.DataFrame:
    keys: list[str] = list(inst.raw_vars.groups) + [inst.ratios_vars.concept_ratio]
    _concept_pos = inst.ratios_vars.concept_pos
    _data_value = inst.raw_vars.value
    pivoted_data = merged_data.pivot(index=keys, on=_concept_pos, values=_data_value)
    return pivoted_data


def augment_data(inst: MungRatio, data: pl.DataFrame) -> pl.DataFrame:
    cols = {
        inst.ratios_vars.concept_num: inst.ratios_vars.value_num,
        inst.ratios_vars.concept_den: inst.ratios_vars.value_den,
    }
    data = data.rename(mapping=cols)
    _concept_ratio = inst.ratios_vars.concept_ratio
    augmented_data = data.join(
        inst.ratios,
        how="inner",
        left_on=_concept_ratio,
        right_on=_concept_ratio,
    )
    return augmented_data


def move_cols(inst: MungRatio, data: pl.DataFrame) -> pl.DataFrame:
    new_cols = [col for col in data.columns if col not in cols] + cols
    data = data.select(new_cols)
    return data
