"""Test the calc_bridge class."""

import pytest
from pathlib import Path
import pandas as pd

from fltk.calc_waterfall.main import CalcWaterfall


@pytest.fixture
def wfall() -> CalcWaterfall:
    return CalcWaterfall(name="test_wfall", initial="relative")

def test_initial_err() -> None:
    with pytest.raises(ValueError):
        CalcWaterfall(name="test_wfall", initial="relativ")


@pytest.fixture
def fixtures_path() -> Path:
    return Path(__file__).parent.joinpath("fixtures")


@pytest.fixture
def raw_data(fixtures_path) -> pd.DataFrame:
    fn = fixtures_path.joinpath("waterfall.xlsx")
    out = pd.read_excel(
        fn,
        sheet_name="data1",
        engine="openpyxl",
        engine_kwargs={"data_only": True},
    )
    return out


def test_load_data(wfall, raw_data) -> None:
    wfall.load_raw_data(
        raw_data,
        groups=("entity", "pertype"),
        period_from="period_from",
        period_to="period_to",
        ratio_nm="concept_ratio",
        num_from_val="num_from",
        num_to_val="num_to",
        volume_diff="vol_diff",
        price_diff="price_diff",
        mix_diff="mix_diff",
        total_diff="tot_diff",
    )
    assert wfall.raw.shape == (27, 21)


@pytest.fixture
def wfall_init(wfall, raw_data):
    wfall.load_raw_data(
        raw_data,
        groups=("entity", "pertype"),
        period_from="period_from",
        period_to="period_to",
        ratio_nm="concept_ratio",
        num_from_val="num_from",
        num_to_val="num_to",
        volume_diff="vol_diff",
        price_diff="price_diff",
        mix_diff="mix_diff",
        total_diff="tot_diff",
    )
    return wfall


def test_fit(wfall_init):
    wfall_init.fit()
    assert wfall_init.base.shape == (162, 9)


def test_fit_transform(wfall_init):
    wfall_init.fit_transform()
    assert wfall_init.wfall.shape == (117, 10)
