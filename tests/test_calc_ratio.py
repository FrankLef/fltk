"""Test the calc_ratio class."""

import pytest
from pathlib import Path
import pandas as pd

# from typing import Any
from fltk.calc_ratio.main import CalcRatio


@pytest.fixture
def ratio() -> CalcRatio:
    return CalcRatio(name="test_ratio")


@pytest.fixture
def fixtures_path() -> Path:
    return Path(__file__).parent.joinpath("fixtures")


@pytest.fixture
def ratios_xl(fixtures_path) -> dict[str, str]:
    out = {"path": fixtures_path.joinpath("ratio.xlsx"), "sheet": "concepts_ratios"}
    return out


@pytest.fixture
def data_xl(fixtures_path) -> dict[str, str]:
    out = {"path": fixtures_path.joinpath("ratio.xlsx"), "sheet": "data1"}
    return out


@pytest.fixture
def raw_data(data_xl) -> pd.DataFrame:
    raw_data = pd.read_excel(
        data_xl["path"],
        sheet_name=data_xl["sheet"],
        engine="openpyxl",
        engine_kwargs={"data_only": True},
    )
    return raw_data


def test_load_ratios(ratio, ratios_xl: dict[str, Path | str]) -> None:
    ratio.load_ratios(path=ratios_xl["path"], sheet_nm=ratios_xl["sheet"])
    assert ratio.ratios_df.shape == (6, 3)


def test_load_data(ratio, raw_data) -> None:
    with pytest.raises(ValueError):
        ratio.load_data(
            raw_data,
            concept_var="concept",
            value_var="amount",
            group_vars=["entity", "pertype", "period"],
        )


@pytest.fixture
def init_ratio(ratio, ratios_xl, raw_data) -> CalcRatio:
    ratio.load_ratios(path=ratios_xl["path"], sheet_nm=ratios_xl["sheet"])
    ratio.load_data(
        raw_data,
        concept_var="concept",
        value_var="amount",
        group_vars=["entity", "pertype", "period"],
    )
    return ratio


def test_init_ratio(init_ratio) -> None:
    assert init_ratio.ratios_df.shape == (6, 3)
    assert init_ratio.ratios_df_long.shape == (12, 3)
    assert init_ratio.data.shape == (21, 5)


def test_fit(init_ratio) -> None:
    init_ratio.fit()
    assert init_ratio.merged_data.shape == (30, 8)


def test_transform(init_ratio) -> None:
    init_ratio.fit()
    init_ratio.transform(is_cleaned=True)
    assert init_ratio.merged_data.shape == (18, 9)
