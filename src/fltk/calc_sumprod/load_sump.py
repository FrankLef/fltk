from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

from ..utils import audit_vars as audit

if TYPE_CHECKING:
    from .main import CalcSumprod  # Only imported when checking types


def load_sump(inst: CalcSumprod, data: pd.DataFrame) -> None:
    if data.empty:
        raise ValueError("Sumproduct dataframe is empty.")
    audit.audit_keys(data, keys=inst.sump_vars.keys)
    # sometimes sump_df is given with extra variables, e.g. pertype. Only keep the reserved_vars. Will give an exception if column does not exist.
    inst.sump = data[list(inst.sump_vars.base)]
