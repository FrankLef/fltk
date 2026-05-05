from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

from ..utils import audit_vars as audit

if TYPE_CHECKING:
    from .main import CalcBridge  # Only imported when checking types


def load_ratios(inst: CalcBridge, data: pd.DataFrame) -> pd.DataFrame:
    if data.empty:
        raise ValueError("The data is empty.")
    audit.audit_cols(data, vars=inst.ratios_vars.vars)
    audit.audit_keys(data, keys=inst.ratios_vars.keys)
    return data