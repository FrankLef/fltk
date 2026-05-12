"""Test the calc_bridge class."""

import pytest
from pathlib import Path
import pandas as pd

from fltk.calc_bridge.main import CalcBridge


@pytest.fixture
def ratios() -> tuple[str, ...]:
    ratios = (
        "Ebitda2TangibleAssetsNoncash",
        "Ebitda2Sales",
        "Sales2TangibleAssetsNoncash",
        "Sales2DirectLabor",
        "Sales2MaterialCosts",
        "MaterialCosts2DirectLabor",
    )
    return ratios


@pytest.fixture
def bridge(ratios) -> CalcBridge:
    return CalcBridge(name="test_bridge", ratios=ratios)


@pytest.fixture
def fixtures_path() -> Path:
    return Path(__file__).parent.joinpath("fixtures")


@pytest.fixture
def raw_data(fixtures_path) -> pd.DataFrame:
    fn = fixtures_path.joinpath("bridge.xlsx")
    out = pd.read_excel(
        fn,
        sheet_name="data1",
        engine="openpyxl",
        engine_kwargs={"data_only": True},
    )
    return out


def test_load_data(bridge, raw_data) -> None:
    bridge.load_raw_data(
        raw_data,
        groups=("entity", "pertype"),
        period="period",
        ratio_nm="concept_ratio",
        ratio_val="ratio",
        num_nm="concept_num",
        num_val="num",
        den_nm="concept_den",
        den_val="den",
    )
    assert bridge.raw.shape == (24, 9)


@pytest.fixture
def bridge_init(bridge, raw_data):
    bridge.load_raw_data(
        raw_data,
        groups=("entity", "pertype"),
        period="period",
        ratio_nm="concept_ratio",
        ratio_val="ratio",
        num_nm="concept_num",
        num_val="num",
        den_nm="concept_den",
        den_val="den",
    )
    return bridge


def test_fit(bridge_init):
    bridge_init.fit()
    assert bridge_init.bridge.shape == (3, 15)


def test_transform(bridge_init):
    bridge_init.fit()
    bridge_init.transform()
    assert bridge_init.bridge.shape == (3, 21)


def test_waterfall(bridge_init):
    bridge_init.fit()
    bridge_init.transform()
    wfall = bridge_init.get_waterfall()
    assert wfall.shape == (18, 7)
