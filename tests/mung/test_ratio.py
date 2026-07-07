"""Test the calc_ratio class."""

import pytest
from pathlib import Path
import polars as pl

from fltk.mung.ratio.main import MungRatio


@pytest.fixture
def fixtures_path() -> Path:
    return Path(__file__).parent.joinpath("fixtures")


@pytest.fixture
def ratios_xl(fixtures_path) -> pl.DataFrame:
    fn = fixtures_path.joinpath("ratio.xlsx")
    out = pl.read_excel(fn, sheet_name="concepts_ratios")
    return out


@pytest.fixture
def ratio(ratios_xl) -> MungRatio:
    return MungRatio(name="test_ratio", data=ratios_xl)


def test_init_ratio(ratio) -> None:
    assert ratio.ratios.shape == (6, 3)
    assert ratio.ratios_long.shape == (12, 3)


@pytest.fixture
def data_xl(fixtures_path) -> dict[str, str]:
    out = {"path": fixtures_path.joinpath("ratio.xlsx"), "sheet": "data1"}
    return out


@pytest.fixture
def raw_data(data_xl) -> pl.DataFrame:
    raw_data = pl.read_excel(data_xl["path"], sheet_name=data_xl["sheet"])
    return raw_data


@pytest.fixture
def init_ratio(ratio, raw_data) -> MungRatio:
    ratio.load_raw_data(
        raw_data,
        concept="concept",
        value="amount",
        groups=("entity", "pertype", "period"),
    )
    return ratio


def test_load_raw(init_ratio) -> None:
    assert init_ratio.ratios.shape == (6, 3)
    assert init_ratio.ratios_long.shape == (12, 3)
    assert init_ratio.raw.shape == (21, 5)


def test_fit(init_ratio) -> None:
    init_ratio.fit()
    assert init_ratio.merged.shape == (30, 8)


def test_fit_transform(init_ratio) -> None:
    init_ratio.fit_transform(is_cleaned=True)
    assert init_ratio.merged.shape == (30, 8)
    assert init_ratio.calc.shape == (30, 9)
