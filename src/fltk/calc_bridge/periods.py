from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from .main import CalcBridge  # Only imported when checking types


def get_periods(
    inst: CalcBridge,
    data: pd.DataFrame
) -> pd.DataFrame:
    _period = inst.raw.period
    _start = inst.periods.start
    _end = inst.periods.end
    return data