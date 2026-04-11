from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd
from pathlib import Path

if TYPE_CHECKING:
    from .main import CalcSumprod  # Only imported when checking types


def load_mat_from_xl(
    inst: CalcSumprod, path: Path, sheet_nm: str | None = None
) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name=sheet_nm)
    top_name = df.columns[0]
    if inst._idx_to != top_name:
        msg: str = f"""
        '{inst._idx_to}' is not the name of the first column in the matrix.
        The name found is '{top_name}'.
        """
        raise KeyError(msg)

    cols = df.columns[df.columns != inst._idx_to].to_list()
    df = df.melt(
        id_vars=inst._idx_to,
        value_vars=cols,
        var_name=inst._idx_from,
        value_name=inst._sump_coef,
    )
    df.dropna(inplace=True)
    return df
