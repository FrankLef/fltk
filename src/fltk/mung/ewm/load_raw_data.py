from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype

from ...utils import audit_vars as audit

if TYPE_CHECKING:
    from .main import CalcEwm  # Only imported when checking types


def load_raw_data(inst: CalcEwm, data: pd.DataFrame) -> pd.DataFrame:
    _vars = inst.raw_vars
    if data.empty:
        raise ValueError("The raw data is empty.")
    audit.audit_missing(data, vars=_vars.vars)
    audit.audit_keys(data, keys=_vars.keys)

    is_err = not is_datetime64_any_dtype(data[_vars.period])
    if is_err:
        dtype = data[_vars.period].dtype
        msg: str = f"Column '{_vars.period}' is of dtype '{dtype}'. It must be of type datetime."
        raise ValueError(msg)

    return data
