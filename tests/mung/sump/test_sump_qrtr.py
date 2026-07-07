"""Test the calc_sumprod class."""

import pytest
from pathlib import Path
import polars as pl
from typing import Any
from fltk.mung.sumprod.main import MungSumprod


@pytest.fixture
def sumprod() -> MungSumprod:
    return MungSumprod(name="test_sumprod", idx_to="idx")


@pytest.fixture
def fixtures_path() -> Path:
    return Path(__file__).parents[1].joinpath("fixtures")


@pytest.fixture
def matrix_xl(fixtures_path) -> dict[str, str]:
    out = {"path": fixtures_path.joinpath("sumprod.xlsx"), "sheet": "qrtr"}
    return out


@pytest.fixture
def data_xl(fixtures_path) -> dict[str, str]:
    out = {"path": fixtures_path.joinpath("sumprod.xlsx"), "sheet": "data1"}
    return out


@pytest.fixture
def raw_data(data_xl) -> pl.DataFrame:
    raw_data = pl.read_excel(data_xl["path"], sheet_name=data_xl["sheet"])
    return raw_data


@pytest.fixture
def data_vars() -> dict[str, Any]:
    out = {
        "idx_var": "period",
        "value_var": "amount",
        "group_vars": ["entity", "concept", "pertype"],
        "newvalue_var": "qrtr_amt",
    }
    return out


def test_err_name() -> None:
    with pytest.raises(ValueError):
        MungSumprod(name=" ", idx_to="idx")
    with pytest.raises(ValueError):
        MungSumprod(name="?", idx_to="idx")


def test_load_mat_xl(sumprod, matrix_xl: dict[str, Path]) -> None:
    sumprod.load_mat_from_xl(path=matrix_xl["path"], sheet_nm=matrix_xl["sheet"])
    assert sumprod.sump.shape == (16, 3)


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
def init_sumprod(sumprod, matrix_xl, raw_data, data_vars) -> MungSumprod:
    sumprod.load_mat_from_xl(path=matrix_xl["path"], sheet_nm=matrix_xl["sheet"])
    sumprod.load_raw_data(
        raw_data,
        idx=data_vars["idx_var"],
        value=data_vars["value_var"],
        groups=data_vars["group_vars"],
        newvalue=data_vars["newvalue_var"],
    )
    return sumprod


def test_init_sumprod(init_sumprod) -> None:
    assert init_sumprod.sump.shape == (16, 3)
    assert init_sumprod.raw.shape == (33, 7)


@pytest.fixture
def final_sumprod(init_sumprod) -> MungSumprod:
    init_sumprod.fit()
    init_sumprod.transform()
    return init_sumprod


def test_incomplete(final_sumprod) -> None:
    assert final_sumprod.incomplete.shape == (11, 6)
    assert final_sumprod.incomplete_uniq.shape == (11, 4)


# @pytest.fixture
# def transform_sumprod(final_sumprod) -> MungSumprod:
#     fi_sumprod.transform()
#     return fit_sumprod


def test_calc(final_sumprod) -> None:
    final_sumprod.calc.shape == (34, 5)
    final_sumprod.calc_aug.shape == (34, 6)
