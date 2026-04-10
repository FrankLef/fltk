from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd
from pathlib import Path

if TYPE_CHECKING:
    from .main import CalcRatio  # Only imported when checking types


def load_ratios(inst: CalcRatio, path: Path, sheet_nm: str | None = None) -> None:
    df = pd.read_excel(
        path,
        sheet_name=sheet_nm,
        engine="openpyxl",
        engine_kwargs={"data_only": True},
    )
    assert not df.empty, "Ratios dataframe is empty."
    validate_ratios_pk(inst, comb_df=df)
    check_null: bool = df.isna().values.any()
    if check_null:
        raise ValueError("Some ratios have empty data.")
    cols = [inst._concept_ratio, inst._concept_num, inst._concept_den]
    check_cols: bool = df.columns.isin(cols).all()
    if not check_cols:
        raise ValueError("Some ratio columns are missing.")
    inst._ratios_df = df
    melt_ratios(inst)


def validate_ratios_pk(inst: CalcRatio, comb_df: pd.Dataframe) -> None:
    pk = inst._concept_ratio
    unique_counts = comb_df[pk].value_counts()
    ndistinct = len(unique_counts)
    if ndistinct != comb_df.shape[0]:
        msg: str = f"Matrix has invalid keys {pk}."
        raise ValueError(msg)


def melt_ratios(inst: CalcRatio) -> None:
    data = inst._ratios_df.copy()
    melted_data = data.melt(
        id_vars=inst._concept_ratio,
        var_name=inst._concept_pos,
        value_name=inst._concept_name,
    )
    inst._ratios_df_long = melted_data
