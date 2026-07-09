"""Test the dic class."""

import pytest
from pathlib import Path

import polars as pl

from fltk.dicz.main import Dicz


@pytest.fixture
def dicz():
    return Dicz(key="dicz_test")


@pytest.fixture
def path():
    return Path(__file__).parent.joinpath("fixtures")


@pytest.fixture
def xlfile(path):
    return path.joinpath("bag_groups.xlsx")


@pytest.fixture
def xlsheet():
    return "data"


def test_dicz(dicz):
    assert isinstance(dicz, Dicz)
    assert dicz.key == "dicz_test"


def test_dicz_append(dicz, xlfile, xlsheet):
    df = pl.read_excel(xlfile, sheet_name=xlsheet)
    dicz.append(key="groups", data=df)
    assert dicz.nbags == 1


@pytest.fixture
def dicz1(dicz, xlfile, xlsheet):
    df = pl.read_excel(xlfile, sheet_name=xlsheet)
    dicz.append(key="groups", data=df)
    return dicz


def test_bag(dicz1, xlfile, xlsheet):
    a_bag = dicz1.bag("groups")
    assert a_bag.ngroups == 2
    assert a_bag.nlines == 18


def test_err_key(dicz1):
    with pytest.raises(KeyError):
        dicz1.bag("X")


def test_group(dicz1):
    a_group = dicz1.bag("groups").group("entities")
    assert a_group.nlines == 5


def test_lines_value(dicz1):
    a_group = dicz1.bag("groups").group("concepts")
    line_keys = ("SalesNet", "MaterialCosts", "AssetsNongoodwillNoncash")
    values = a_group.lines_value(line_keys=line_keys, item_nm="color")
    assert len(values) == len(line_keys)
