from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from .main import CalcRatio  # Only imported when checking types


def get_valid_data(inst: CalcRatio) -> pd.DataFrame:
    # NOTE: Placeholder, to be used later. Should use merged_data as input.
    return inst._merged_data
