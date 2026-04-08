from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from .calc_comb import CalcComb  # Only imported when checking types


def load_combs(inst: CalcComb, data: pd.DataFrame) -> None:
    validate_comb_keys(inst, data)
    inst._comb_df = data


def validate_comb_keys(inst: CalcComb, comb_df: pd.Dataframe) -> None:
    keys = [inst._idx_to, inst._idx_from]
    unique_counts = comb_df[keys].value_counts()
    ndistinct = len(unique_counts)
    if ndistinct != comb_df.shape[0]:
        msg: str = f"Combinations df has invalid keys {keys}."
        raise ValueError(msg)
    inst._comb_keys = keys
