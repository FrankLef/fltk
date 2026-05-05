from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

from ..utils import audit_vars as audit

if TYPE_CHECKING:
    from .main import CalcRatio  # Only imported when checking types


def load_ratios(inst: CalcRatio, data: pd.Dataframe) -> None:
    assert not data.empty, "Ratios dataframe is empty."

    audit.audit_cols(data, vars=inst.ratios_vars.base)
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
    inst.ratios = data
    melt_ratios(inst)


def melt_ratios(inst: CalcRatio) -> None:
    data = inst.ratios.copy()
    melted_data = data.melt(
        id_vars=inst.ratios_vars.concept_ratio,
        var_name=inst.ratios_vars.concept_pos,
        value_name=inst.ratios_vars.concept_name,
    )
    inst.ratios_long = melted_data
