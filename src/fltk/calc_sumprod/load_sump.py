from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from .main import CalcSumprod  # Only imported when checking types


def load_sump(inst: CalcSumprod, data: pd.DataFrame) -> None:
    if data.empty:
        raise ValueError("Sumproduct dataframe is empty.")
    validate_sump_keys(inst, sump_df=data)
    # sometimes sump_df is given with extra variables, e.g. pertype. Only keep the reserved_vars. Will give an exception if column does not exist.
    inst._sump_df = data[inst._sump_vars_base]


def validate_sump_keys(inst: CalcSumprod, sump_df: pd.Dataframe) -> None:
    keys = inst._sump_keys
    unique_counts = sump_df[keys].value_counts()
    if len(unique_counts) != sump_df.shape[0]:
        msg: str = f"Sumproduct data has invalid keys {keys}."
        raise KeyError(msg)
