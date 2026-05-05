from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from .main import CalcRatio  # Only imported when checking types


def calculate(inst: CalcRatio) -> pd.DataFrame:
    data = inst.valid

    data[inst.ratios_vars.value_ratio] = (
        data[inst.ratios_vars.value_num] / data[inst.ratios_vars.value_den]
    )
    return data
