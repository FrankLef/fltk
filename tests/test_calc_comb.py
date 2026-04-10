"""Test the calc_comb class."""

import pytest
from pathlib import Path
import pandas as pd
from typing import Any
from fltk.calc_comb.main import CalcComb


@pytest.fixture
def comb() -> CalcComb:
    return CalcComb(name="test_comb", idx_to="idx")


@pytest.fixture
def fixtures_path() -> Path:
    return Path(__file__).parent.joinpath("fixtures")


@pytest.fixture
def qrtr_mat_xl(fixtures_path) -> dict[str, str]:
    out = {"path": fixtures_path.joinpath("comb.xlsx"), "sheet": "qrtr"}
    return out


@pytest.fixture
def rolly_mat_xl(fixtures_path) -> dict[str, str]:
    out = {"path": fixtures_path.joinpath("comb.xlsx"), "sheet": "rolly"}
    return out


@pytest.fixture
def data_xl(fixtures_path) -> dict[str, str]:
    out = {"path": fixtures_path.joinpath("comb.xlsx"), "sheet": "data1"}
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


def test_err_name() -> CalcComb:
    with pytest.raises(ValueError):
        CalcComb(name=" ", idx_to="idx")
    with pytest.raises(ValueError):
        CalcComb(name="?", idx_to="idx")


def test_load_mat_xl(comb, qrtr_mat_xl: dict[str, Path]) -> None:
    comb.load_mat_from_xl(path=qrtr_mat_xl["path"], sheet_nm=qrtr_mat_xl["sheet"])
    assert comb.combs_df.shape == (16, 3)


def test_load_data(comb, raw_data, data_vars) -> None:
    with pytest.raises(ValueError):
        comb.load_data(
            raw_data,
            idx_var=data_vars["idx_var"],
            value_var=data_vars["value_var"],
            group_vars=data_vars["group_vars"],
            newvalue_var=data_vars["newvalue_var"],
        )


@pytest.fixture
def init_comb(comb, qrtr_mat_xl, raw_data, data_vars) -> CalcComb:
    comb.load_mat_from_xl(path=qrtr_mat_xl["path"], sheet_nm=qrtr_mat_xl["sheet"])
    comb.load_data(
        raw_data,
        idx_var=data_vars["idx_var"],
        value_var=data_vars["value_var"],
        group_vars=data_vars["group_vars"],
        newvalue_var=data_vars["newvalue_var"],
    )
    return comb


def test_init_comb(init_comb) -> None:
    assert init_comb.combs_df.shape == (16, 3)
    assert init_comb.data.shape == (33, 7)


@pytest.fixture
def fit_comb(init_comb) -> CalcComb:
    init_comb.fit()
    return init_comb


def test_fit_comb(fit_comb) -> None:
    assert fit_comb.invalid_data.shape == (3, 6)
    # assert fit_comb.undetermined_data.shape == (1, 4)


@pytest.fixture
def transform_comb(fit_comb) -> CalcComb:
    fit_comb.transform(is_merged=True)
    return fit_comb


def test_transform_comb(transform_comb) -> None:
    transform_comb.valid_data.shape == (25, 6)
