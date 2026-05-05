from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

from ..utils import audit_vars as audit

if TYPE_CHECKING:
    from .main import CalcRatio  # Only imported when checking types


def load_raw_data(inst: CalcRatio, data: pd.DataFrame) -> pd.DataFrame:
    if inst.ratios.empty:
        msg: str = "You must load the ratio definitions before the data."
        raise ValueError(msg)
    if data.empty:
        raise ValueError("The raw data is empty.")
    audit.audit_illegal(data, vars=inst.ratios_vars)
    audit.audit_keys(data, keys=inst.raw_vars.keys)
    all_vars = list(inst.raw_vars.vars)
    reduced_data = data[all_vars]
    return reduced_data
