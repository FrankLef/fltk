from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from .main import CalcBridge  # Only imported when checking types


def get_periods(inst: CalcBridge) -> pd.DataFrame:
    _data = inst.raw
    _period = inst.raw_vars.period
    _start = inst.periods_vars.start
    _end = inst.periods_vars.end

    the_periods = sorted(_data[_period].unique())
    assert len(the_periods) >= 2, "There must be at least 2 distinct periods."
    the_starts = the_periods[:-1]
    the_ends = the_periods[1:]
    periods_df = pd.DataFrame({_start: the_starts, _end: the_ends})
    assert not periods_df.empty, "Periods df is empty!"
    return periods_df
