from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from .calc_ratio import CalcRatio  # Only imported when checking types


def get_invalid_data(inst: CalcRatio) -> pd.DataFrame:
    data = inst._data
    get_missing_data(inst, data=data)
    return pd.DataFrame()


def get_missing_data(inst: CalcRatio, data: pd.DataFrame) -> pd.DataFrame:
    # ratios_df = inst._ratios_df
    # data.merge(ratios_df, show="left", left_on=inst._data_concept, right_on=inst._concept_num)
    # breakpoint()
    return pd.DataFrame()
