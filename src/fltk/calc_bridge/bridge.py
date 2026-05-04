from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from .main import CalcBridge  # Only imported when checking types


def get_bridge(inst: CalcBridge) -> pd.DataFrame:
    _data = inst.raw_df
    _periods = inst.periods_df
    return _data
