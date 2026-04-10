from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from .main import CalcComb  # Only imported when checking types


def load_combs(inst: CalcComb, data: pd.DataFrame) -> None:
    if data.empty:
        raise ValueError("Combs dataframe is empty.")
    validate_comb_keys(inst, combs_df=data)
    # sometimes combs_df is given with extra variables, e.g. pertype. Only keep the reserved_vars. Will give an eexception if column does not exist.
    inst._combs_df = data[inst._comb_vars_base]


def validate_comb_keys(inst: CalcComb, combs_df: pd.Dataframe) -> None:
    keys = inst._comb_keys
    unique_counts = combs_df[keys].value_counts()
    if len(unique_counts) != combs_df.shape[0]:
        msg: str = f"Combinations df has invalid keys {keys}."
        raise KeyError(msg)
