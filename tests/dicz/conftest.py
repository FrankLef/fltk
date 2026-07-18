import pytest
from pathlib import Path
import polars as pl

from fltk.dicz.main import Dicz

# https://stackoverflow.com/questions/34466027/what-is-conftest-py-for-in-pytest


@pytest.fixture
def path() -> Path:
    return Path(__file__).parent.joinpath("fixtures")


@pytest.fixture
def dicz1_() -> Dicz:
    return Dicz(key="dicz1")


@pytest.fixture
def groups_xl(path) -> Path:
    return path.joinpath("bag_groups.xlsx")


@pytest.fixture
def xbr_xl(path) -> Path:
    return path.joinpath("bag_xbr.xlsx")


@pytest.fixture
def dicz1(groups_xl, xbr_xl) -> Dicz:
    dicz1 = Dicz(key="dicz1")
    dfs = {"groups": groups_xl, "xbr": xbr_xl}
    for key, xl in dfs.items():
        df = pl.read_excel(xl, sheet_name="data")
        dicz1.append(key=key, data=df)
    return dicz1
