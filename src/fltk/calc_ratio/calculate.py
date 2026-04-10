from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from .main import CalcRatio  # Only imported when checking types


def calculate(inst: CalcRatio) -> pd.DataFrame:
    data = inst._merged_data
    data[inst._value_ratio] = data[inst._value_num] / data[inst._value_den]
    return data
