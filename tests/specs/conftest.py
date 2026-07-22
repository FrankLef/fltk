import pytest
from pathlib import Path
import polars as pl

from fltk.specs.specs_mastr import SpecsMastr

# https://stackoverflow.com/questions/34466027/what-is-conftest-py-for-in-pytest


@pytest.fixture
def path() -> Path:
    return Path(__file__).parent.joinpath("fixtures")


@pytest.fixture
def groups_xl(path) -> Path:
    return path.joinpath("specs_groups.xlsx")


@pytest.fixture
def xbr_xl(path) -> Path:
    return path.joinpath("specs_xbr.xlsx")


@pytest.fixture
def mastr1(groups_xl, xbr_xl) -> SpecsMastr:
    specs_mastr1 = SpecsMastr(name="specs_mastr1")
    dfs = {"groups": groups_xl, "xbr": xbr_xl}
    for specs_nm, xl in dfs.items():
        df = pl.read_excel(xl, sheet_name="data")
        specs_mastr1.append(specs_nm=specs_nm, data=df)
    return specs_mastr1
