from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import polars as pl

from ...utils import audit_vars as audit

if TYPE_CHECKING:
    from .main import MungEwm  # Only imported when checking types


def load_raw_data(inst: MungEwm, data: pl.DataFrame) -> pl.DataFrame:
    _vars = inst.raw_vars
    if data.is_empty():
        raise ValueError("The raw data is empty.")
    audit.audit_missing(data, vars=_vars.vars)

    return data
