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
    _idx_to = inst.sump_vars.idx_to
    _idx_from = inst.sump_vars.idx_from
    _sump_coef = inst.sump_vars.sump_coef
    if _idx_to != top_name:
        msg: str = f"""
        '{_idx_to}' is not the name of the first column in the matrix.
        The name found is '{top_name}'.
        """
        raise KeyError(msg)

    cols = df.columns[df.columns != _idx_to].to_list()
    df = df.melt(
        id_vars=_idx_to,
        value_vars=cols,
        var_name=_idx_from,
        value_name=_sump_coef,
    )
    df.dropna(inplace=True)
    return df
