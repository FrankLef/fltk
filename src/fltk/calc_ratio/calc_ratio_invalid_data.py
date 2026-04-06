from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from .calc_ratio import CalcRatio  # Only imported when checking types


def get_invalid_data(inst: CalcRatio) -> pd.DataFrame:
    return pd.DataFrame()