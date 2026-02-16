"""Test the diffmat class."""

import pytest
from pathlib import Path
import pandas as pd
from typing import Any
from fltk.diffmat.diffmat import DiffMat


@pytest.fixture
def diffmat() -> DiffMat:
    return DiffMat(idx_to="idx")


@pytest.fixture
def fixtures_path() -> Path:
    return Path(__file__).parent.joinpath("fixtures")


@pytest.fixture
def qrtr_mat_xl(fixtures_path) -> dict[str, str]:
    out = {"path": fixtures_path.joinpath("diffmat.xlsx"), "sheet": "qrtr"}
    return out


@pytest.fixture
def rolly_mat_xl(fixtures_path) -> dict[str, str]:
    out = {"path": fixtures_path.joinpath("diffmat.xlsx"), "sheet": "rolly"}
    return out


@pytest.fixture
def data_xl(fixtures_path) -> dict[str, str]:
    out = {"path": fixtures_path.joinpath("diffmat.xlsx"), "sheet": "data1"}
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


def test_load_mat_xl(diffmat, qrtr_mat_xl: dict[str, Path]) -> None:
    diffmat.load_mat_from_xl(path=qrtr_mat_xl["path"], sheet_nm=qrtr_mat_xl["sheet"])
    assert diffmat.idx_df.shape == (16, 3)


def test_load_data(diffmat, raw_data, data_vars) -> None:
    with pytest.raises(ValueError):
        diffmat.load_data(
            raw_data,
            idx_var=data_vars["idx_var"],
            value_var=data_vars["value_var"],
            group_vars=data_vars["group_vars"],
            newvalue_var=data_vars["newvalue_var"],
        )


@pytest.fixture
def init_diffmat(diffmat, qrtr_mat_xl, raw_data, data_vars) -> DiffMat:
    diffmat.load_mat_from_xl(path=qrtr_mat_xl["path"], sheet_nm=qrtr_mat_xl["sheet"])
    diffmat.load_data(
        raw_data,
        idx_var=data_vars["idx_var"],
        value_var=data_vars["value_var"],
        group_vars=data_vars["group_vars"],
        newvalue_var=data_vars["newvalue_var"],
    )
    return diffmat


def test_init_diffmat(init_diffmat) -> None:
    assert init_diffmat.idx_df.shape == (16, 3)
    assert init_diffmat.data.shape == (33, 7)


@pytest.fixture
def fit_diffmat(init_diffmat) -> DiffMat:
    init_diffmat.fit()
    return init_diffmat


def test_fit_diffmat(fit_diffmat) -> None:
    assert fit_diffmat.invalid_data.shape == (3, 6)
    assert fit_diffmat.undetermined_data.shape == (1, 4)


@pytest.fixture
def transform_diffmat(fit_diffmat) -> DiffMat:
    fit_diffmat.transform()
    return fit_diffmat


def test_transform_diffmat(transform_diffmat) -> None:
    transform_diffmat.valid_data.shape == (25, 6)
