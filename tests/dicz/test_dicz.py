"""Test the dic class."""

import pytest
from pathlib import Path

# import pandas as pd
import polars as pl

from fltk.dicz.main import Dicz


@pytest.fixture
def dicz():
    return Dicz(name="dicz_test")


@pytest.fixture
def path():
    return Path(__file__).parent


@pytest.fixture
def xlfile(path):
    return path.joinpath("bag1.xlsx")


@pytest.fixture
def xlsheet():
    return "data1"


def test_dicz(dicz):
    assert isinstance(dicz, Dicz)
    assert dicz.name == "dicz_test"


def test_dicz_append(dicz, xlfile, xlsheet):
    df = pl.read_excel(xlfile, sheet_name=xlsheet)
    dicz.append(key="bag1", data=df)
    assert dicz.nbags == 1


@pytest.fixture
def dicz1(dicz, xlfile, xlsheet):
    df = pl.read_excel(xlfile, sheet_name=xlsheet)
    dicz.append(key="bag1", data=df)
    return dicz


def test_bag(dicz1, xlfile, xlsheet):
    a_bag = dicz1.bag("bag1")
    assert a_bag.ngroups == 2
    assert a_bag.nlines == 18


def test_err_key(dicz1):
    with pytest.raises(KeyError):
        dicz1.bag("X")


def test_group(dicz1):
    a_group = dicz1.bag("bag1").group("entities")
    assert a_group.nlines == 5


def test_lines_value(dicz1):
    a_group = dicz1.bag("bag1").group("concepts")
    line_keys = ("SalesNet", "MaterialCosts", "AssetsNongoodwillNoncash")
    values = a_group.lines_value(line_keys=line_keys, item_nm="color")
    assert len(values) == len(line_keys)
