from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from .diffmat import DiffMat  # Only imported when checking types


def calculate(inst: DiffMat) -> pd.DataFrame:
    # value_var = inst._data_value
    newvalue_var = inst._data_newvalue
    data = inst._valid_data
    # idx_df = inst.idx_df
    data[newvalue_var] = pd.NA
    return data
