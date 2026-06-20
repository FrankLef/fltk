from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

from ...utils import audit_vars as audit

if TYPE_CHECKING:
    from .main import MungRatio  # Only imported when checking types


def load_ratios(inst: MungRatio, data: pd.Dataframe) -> pd.DataFrame:
    if data.empty:
        raise ValueError("Ratios dataframe is empty.")

    audit.audit_missing(data, vars=inst.ratios_vars.base)
    audit.audit_keys(data, keys=inst.ratios_vars.keys)
    check_null: bool = data.isna().values.any()
    if check_null:
        raise ValueError("Some ratios have empty data.")
    _concept_ratio = inst.ratios_vars.concept_ratio
    _concept_num = inst.ratios_vars.concept_num
    _concept_den = inst.ratios_vars.concept_den
    cols = [_concept_ratio, _concept_num, _concept_den]
    check_cols: bool = data.columns.isin(cols).all()
    if not check_cols:
        raise ValueError("Some ratio columns are missing.")
    return data


def melt_ratios(
    data: pd.DataFrame, concept_ratio: str, concept_nm: str, concept_pos: str
) -> pd.DataFrame:
    audit.audit_illegal(data, vars=(concept_nm, concept_pos))
    melted_data = data.melt(
        id_vars=concept_ratio,
        var_name=concept_pos,
        value_name=concept_nm,
    )
    return melted_data
