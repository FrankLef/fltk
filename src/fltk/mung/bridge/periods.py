from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from .main import MungBridge  # Only imported when checking types


def get_periods(inst: MungBridge) -> pd.DataFrame:
    _data = inst.raw
    _period = inst.raw_vars.period
    _periods = inst.periods_vars

    the_periods = sorted(_data[_period].unique())
    if len(the_periods) < 2:
        raise ValueError("There must be at least 2 distinct periods.")
    the_starts = the_periods[:-1]
    the_ends = the_periods[1:]
    periods_df = pd.DataFrame({_periods.start: the_starts, _periods.end: the_ends})
    assert not periods_df.empty, "Periods df is empty!"
    return periods_df
