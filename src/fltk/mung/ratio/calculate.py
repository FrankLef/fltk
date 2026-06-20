from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from .main import MungRatio  # Only imported when checking types


def calculate(inst: MungRatio) -> pd.DataFrame:
    data = inst.merged.copy()

    data[inst.ratios_vars.value_ratio] = (
        data[inst.ratios_vars.value_num] / data[inst.ratios_vars.value_den]
    )
    return data
