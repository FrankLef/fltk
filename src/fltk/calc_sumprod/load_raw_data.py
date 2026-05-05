from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd
from rich.prompt import Confirm

from ..utils import audit_vars as audit

if TYPE_CHECKING:
    from .main import CalcSumprod  # Only imported when checking types


def load_raw_data(inst: CalcSumprod, data: pd.DataFrame) -> pd.DataFrame:
    
    if inst.sump.empty:
        msg: str = "You must load the matrix before the data."
        raise ValueError(msg)
    validate_data_names(inst, data=data, newvalue_var=inst.raw_vars.newvalue)
    audit.audit_keys(data, keys=inst.raw_vars.keys)
    return data


def validate_data_names(
    inst: CalcSumprod, data: pd.DataFrame, newvalue_var: str
) -> None:
    cols = data.columns.to_list()
    if newvalue_var in cols:
        msg: str = f"'{newvalue_var}' will be replaced with new calculations?"
        if not Confirm.ask(msg, default=True):
            msg = f"Cancelled by user because of '{newvalue_var}'."
            raise ValueError(msg)
    else:
        cols.append(newvalue_var)
    illegal_vars = [var for var in cols if var in inst.sump_vars.vars]
    if illegal_vars:
        msg = f"""
        {illegal_vars} are reserved names.
        Please change these column names.
        """
        raise ValueError(msg)

    invalid_vars = [var for var in inst.raw_vars.vars if var not in cols]
    if invalid_vars:
        raise KeyError(f"{invalid_vars} are not in data columns.")