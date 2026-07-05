from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import polars as pl

from ...utils import audit_vars as audit

if TYPE_CHECKING:
    from .main import MungBridge  # Only imported when checking types


def load_raw_data(inst: MungBridge, data: pl.DataFrame) -> pl.DataFrame:
    if data.is_empty():
        raise ValueError("The raw data is empty.")
    audit.audit_missing(data, vars=inst.raw_vars.vars)
    # audit.audit_keys(data, keys=inst.raw_vars.keys)
    return data
