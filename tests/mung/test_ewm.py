"""Test the calc_ewm class."""

import pytest
from pathlib import Path
import polars as pl

from fltk.mung.ewm.main import MungEwm


@pytest.fixture
def ewm() -> MungEwm:
    return MungEwm(name="test_ewm")


@pytest.fixture
def fixtures_path() -> Path:
    return Path(__file__).parent.joinpath("fixtures")


@pytest.fixture
def raw_data(fixtures_path) -> pl.DataFrame:
    fn = fixtures_path.joinpath("ewm.xlsx")
    out = pl.read_excel(fn, sheet_name="data1")
    return out


def test_load_data(ewm, raw_data) -> None:
    ewm.load_raw_data(
        raw_data,
        groups=("entity", "concept"),
        period="period",
        values=("cum", "qrtr"),
    )
    assert ewm.raw.shape == (32, 5)


@pytest.fixture
def ewm_init(ewm, raw_data):
    ewm.load_raw_data(
        raw_data,
        groups=("entity", "concept"),
        period="period",
        values=("cum", "qrtr"),
    )
    return ewm


def test_fit_transform(ewm_init):
    ewm_init.fit_transform()
    assert ewm_init.ewm.shape == (32, 7)
