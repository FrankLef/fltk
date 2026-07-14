"""Test the calc_sumprod class."""

import pytest
from pathlib import Path
import polars as pl
from typing import Any
from fltk.mung.sumprod.main import MungSumprod

newvalue_nm: str = "adds_amt"


@pytest.fixture
def sumprod() -> MungSumprod:
    return MungSumprod(
        name="test_adds",
        idx_to="concept_add",
        idx_from="concept_addend",
        sump_coef="coef",
        sump_value="sum_amt",
    )


@pytest.fixture
def fixtures_path() -> Path:
    return Path(__file__).parents[1].joinpath("fixtures")


@pytest.fixture
def data_xl(fixtures_path) -> dict[str, str]:
    out = {"path": fixtures_path.joinpath("sumprod.xlsx"), "sheet": "data1"}
    return out


@pytest.fixture
def raw_data(fixtures_path) -> pl.DataFrame:
    path = fixtures_path.joinpath("sumprod.xlsx")
    raw_data = pl.read_excel(path, sheet_name="data2")
    return raw_data


@pytest.fixture
def sump_df(fixtures_path) -> pl.DataFrame:
    path = fixtures_path.joinpath("sumprod.xlsx")
    sump_df = pl.read_excel(path, sheet_name="concepts_adds")
    return sump_df


def test_load_sump(sumprod, sump_df) -> None:
    sumprod.load_sump(sump_df)
    sumprod.sump.shape == (26, 4)


@pytest.fixture
def data_vars() -> dict[str, Any]:
    out = {
        "idx_var": "concept",
        "value_var": "amount",
        "group_vars": ("entity", "period", "pertype"),
        "newvalue_var": newvalue_nm,
    }
    return out


def test_load_data(sumprod, raw_data, data_vars) -> None:
    with pytest.raises(ValueError):
        sumprod.load_raw_data(
            raw_data,
            idx=data_vars["idx_var"],
            value=data_vars["value_var"],
            groups=data_vars["group_vars"],
            newvalue=data_vars["newvalue_var"],
        )


@pytest.fixture
def init_sumprod(sumprod, sump_df, raw_data, data_vars) -> MungSumprod:
    sumprod.load_sump(sump_df)
    sumprod.load_raw_data(
        raw_data,
        idx=data_vars["idx_var"],
        value=data_vars["value_var"],
        groups=data_vars["group_vars"],
        newvalue=data_vars["newvalue_var"],
    )
    return sumprod


def test_init_sumprod(init_sumprod) -> None:
    assert init_sumprod.sump.shape == (26, 4)
    assert init_sumprod.raw.shape == (22, 6)


@pytest.fixture
def final_sumprod(init_sumprod) -> MungSumprod:
    init_sumprod.fit()
    init_sumprod.transform(missing_to_zero=True)
    return init_sumprod


def test_calc(final_sumprod) -> None:
    calc_df = final_sumprod.calc
    assert calc_df.shape == (42, 5)
    assert calc_df[newvalue_nm].null_count() == 0
    assert calc_df[newvalue_nm].sum() == 5560
