"""Test the calc_comb class."""

import pytest
from pathlib import Path
import pandas as pd
from typing import Any
from fltk.calc_sumprod.main import CalcSumprod


@pytest.fixture
def sumprod() -> CalcSumprod:
    return CalcSumprod(name="test_sumprod", idx_to="idx")


@pytest.fixture
def fixtures_path() -> Path:
    return Path(__file__).parent.joinpath("fixtures")


@pytest.fixture
def qrtr_mat_xl(fixtures_path) -> dict[str, str]:
    out = {"path": fixtures_path.joinpath("sumprod.xlsx"), "sheet": "qrtr"}
    return out


@pytest.fixture
def rolly_mat_xl(fixtures_path) -> dict[str, str]:
    out = {"path": fixtures_path.joinpath("sumprod.xlsx"), "sheet": "rolly"}
    return out


@pytest.fixture
def data_xl(fixtures_path) -> dict[str, str]:
    out = {"path": fixtures_path.joinpath("sumprod.xlsx"), "sheet": "data1"}
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


@pytest.fixture
def data_vars() -> dict[str, Any]:
    out = {
        "idx_var": "period",
        "value_var": "amount",
        "group_vars": ["entity", "concept", "pertype"],
        "newvalue_var": "qrtr_amt",
    }
    return out


def test_err_name() -> CalcSumprod:
    with pytest.raises(ValueError):
        CalcSumprod(name=" ", idx_to="idx")
    with pytest.raises(ValueError):
        CalcSumprod(name="?", idx_to="idx")


def test_load_mat_xl(sumprod, qrtr_mat_xl: dict[str, Path]) -> None:
    sumprod.load_mat_from_xl(path=qrtr_mat_xl["path"], sheet_nm=qrtr_mat_xl["sheet"])
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
def init_sumprod(sumprod, qrtr_mat_xl, raw_data, data_vars) -> CalcSumprod:
    sumprod.load_mat_from_xl(path=qrtr_mat_xl["path"], sheet_nm=qrtr_mat_xl["sheet"])
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
def fit_sumprod(init_sumprod) -> CalcSumprod:
    init_sumprod.fit(is_fillna=False)
    return init_sumprod


def test_fit_sumprod(fit_sumprod) -> None:
    assert fit_sumprod.invalid.shape == (3, 6)


@pytest.fixture
def transform_sumprod(fit_sumprod) -> CalcSumprod:
    fit_sumprod.transform(is_merged=True)
    return fit_sumprod


def test_transform_sumprod(transform_sumprod) -> None:
    transform_sumprod.output.shape == (25, 6)
