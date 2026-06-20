from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd


if TYPE_CHECKING:
    from .main import MungEwm  # Only imported when checking types


def get_base(inst: MungEwm) -> pd.DataFrame:
    _raw = inst.raw_vars

    data = inst.raw.copy()

    data.sort_values(_raw.period, ascending=True, inplace=True)

    return data
