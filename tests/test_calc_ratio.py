"""Test the calc_ratio class."""

import pytest
from pathlib import Path
import pandas as pd

from fltk.calc_ratio.main import CalcRatio


@pytest.fixture
def ratio() -> CalcRatio:
    return CalcRatio(name="test_ratio")


@pytest.fixture
def fixtures_path() -> Path:
    return Path(__file__).parent.joinpath("fixtures")


@pytest.fixture
def ratios_xl(fixtures_path) -> pd.DataFrame:
    fn = fixtures_path.joinpath("ratio.xlsx")
    out = pd.read_excel(
        fn,
        sheet_name="concepts_ratios",
        engine="openpyxl",
        engine_kwargs={"data_only": True},
    )
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
    ratio.load_ratios(ratios_xl)
    assert ratio.ratios.shape == (6, 3)


def test_load_data(ratio, raw_data) -> None:
    with pytest.raises(ValueError):
        ratio.load_raw_data(
            raw_data,
            concept="concept",
            value="amount",
            groups=("entity", "pertype", "period"),
        )


@pytest.fixture
def init_ratio(ratio, ratios_xl, raw_data) -> CalcRatio:
    ratio.load_ratios(ratios_xl)
    ratio.load_raw_data(
        raw_data,
        concept="concept",
        value="amount",
        groups=("entity", "pertype", "period"),
    )
    return ratio


def test_init_ratio(init_ratio) -> None:
    assert init_ratio.ratios.shape == (6, 3)
    assert init_ratio.ratios_long.shape == (12, 3)
    assert init_ratio.raw.shape == (21, 5)


def test_fit(init_ratio) -> None:
    init_ratio.fit()
    assert init_ratio.merged.shape == (30, 8)


def test_transform(init_ratio) -> None:
    init_ratio.fit()
    init_ratio.transform(is_cleaned=True)
    assert init_ratio.merged.shape == (18, 9)
    assert init_ratio.calc.shape == (18, 9)
