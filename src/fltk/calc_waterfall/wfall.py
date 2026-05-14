from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from .main import CalcWaterfall  # Only imported when checking types


def get_wfall(inst: CalcWaterfall) -> pd.DataFrame:
    wfall = inst.base.copy()
    return wfall