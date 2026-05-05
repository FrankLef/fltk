from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from .main import CalcBridge  # Only imported when checking types


def calculate(inst: CalcBridge) -> pd.DataFrame:
    _bridge = inst.bridge_df
    return _bridge
