from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import polars as pl


if TYPE_CHECKING:
    from .main import MungSumprod  # Only imported when checking types


def load_sump(inst: MungSumprod, data: pl.DataFrame) -> None:
    if data.is_empty():
        raise ValueError("Sumproduct dataframe is empty.")
    sort_vars = inst.sump_vars.base
    data = data.sort(sort_vars)
    # sometimes sump_df is given with extra variables, e.g. pertype. Only keep the reserved_vars. Will give an exception if column does not exist.
    # inst.sump = data.select(pl.col(inst.sump_vars.base))
    # inst.sump = data[list(inst.sump_vars.base)]
    inst.sump = data
