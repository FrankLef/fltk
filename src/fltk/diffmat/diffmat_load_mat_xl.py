from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd
from pathlib import Path

if TYPE_CHECKING:
    from .diffmat import DiffMat  # Only imported when checking types


def load_mat_from_xl(inst: DiffMat, path: Path, sheet_nm: str | None = None) -> None:
    df = pd.read_excel(path, sheet_name=sheet_nm)
    cols = df.columns[df.columns != inst._idx_to].to_list()
    df = df.melt(
        id_vars=inst._idx_to,
        value_vars=cols,
        var_name=inst._idx_from,
        value_name=inst._idx_coef
    )
    df.dropna(inplace=True)
    validate_idx_keys(inst, df)
    inst._idx_df = df


def validate_idx_keys(inst: DiffMat, idx_df: pd.Dataframe) -> None:
    keys = [inst._idx_to, inst._idx_from]
    unique_counts = idx_df[keys].value_counts()
    ndistinct = len(unique_counts)
    if ndistinct != idx_df.shape[0]:
        msg: str = f"Matrix has invalid keys {keys}."
        raise ValueError(msg)
    inst._idx_keys = keys
