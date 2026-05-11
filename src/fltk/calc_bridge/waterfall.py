from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING, Final
import pandas as pd
from pandas.api.types import CategoricalDtype

if TYPE_CHECKING:
    from .main import CalcBridge  # Only imported when checking types


def get_waterfall(inst: CalcBridge) -> pd.DataFrame:
    DIFF_NM: Final[str] = "diff_nm"
    DIFF_VAL: Final[str] = "diff_val"
    if inst.bridge.empty:
        raise ValueError("Bridge data is empty.")
    _groups = inst.raw_vars.groups
    _concept_ratio = inst.raw_vars.ratio_nm
    _period_nms = inst.add_suffix(inst.raw_vars.period)
    
    keys: list[str] = list(_groups) + [_concept_ratio] + list(_period_nms)
    wfall_factors = list(get_factors(inst))
    cols = keys + wfall_factors
    
    data_wide = inst.bridge.copy()
    data_wide = data_wide[cols]
    
    data_long = data_wide.melt(
        id_vars=keys, value_vars=wfall_factors, var_name=DIFF_NM, value_name=DIFF_VAL)
    cat_type = CategoricalDtype(categories=wfall_factors, ordered=True)
    data_long[DIFF_NM] = data_long[DIFF_NM].astype(cat_type)
    
    return data_long


def get_factors(inst: CalcBridge) -> tuple[str, ...]:
    _concept_num_nms = inst.add_suffix(inst.raw_vars.num_val)
    vars = inst.bridge_vars
    wfall_factors = (
        _concept_num_nms[0],
        vars.price_diff,
        vars.volume_diff,
        vars.mix_diff,
        vars.total_diff,
        _concept_num_nms[1])
    return wfall_factors
    