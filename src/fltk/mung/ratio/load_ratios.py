from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import polars as pl

from ...utils import audit_vars as audit

if TYPE_CHECKING:
    from .main import MungRatio  # Only imported when checking types


def load_ratios(inst: MungRatio, data: pl.DataFrame) -> pl.DataFrame:
    if data.is_empty():
        raise ValueError("Ratios dataframe is empty.")

    audit.audit_missing(data, vars=inst.ratios_vars.base)
    return data


def melt_ratios(
    data: pl.DataFrame, concept_ratio: str, concept_nm: str, concept_pos: str
) -> pl.DataFrame:
    audit.audit_illegal(data, vars=(concept_nm, concept_pos))
    melted_data = data.unpivot(
        index=concept_ratio,
        variable_name=concept_pos,
        value_name=concept_nm,
    )
    return melted_data
