"""Test the dic class."""

import pytest
from pathlib import Path
import pandas as pd
from fltk.dicz.main import Dicz


@pytest.fixture
def dicz():
    return Dicz(name="dicz_test")


@pytest.fixture
def path():
    return Path(__file__).parent


@pytest.fixture
def xlfile(path):
    return path.joinpath("dicz1.xlsx")


@pytest.fixture
def xlsheet():
    return "data1"


def test_dicz(dicz):
    assert isinstance(dicz, Dicz)
    assert dicz.name == "dicz_test"


def test_dicts(dicz, xlfile, xlsheet):
    df = pd.read_excel(xlfile, sheet_name=xlsheet)
    dicz.get_dicts(df)
    assert dicz.ngroups == 2
    assert dicz.nlines == 18


def test_build(dicz, xlfile, xlsheet):
    df = pd.read_excel(xlfile, sheet_name=xlsheet)
    dicz.build(df)
    assert dicz.ngroups == 2
    assert dicz.nlines == 18


@pytest.fixture
def dicz1(dicz, xlfile, xlsheet):
    df = pd.read_excel(xlfile, sheet_name=xlsheet)
    dicz.build(df)
    return dicz


def test_err_key(dicz1):
    with pytest.raises(KeyError):
        dicz1.group("X")
        
def test_filter_role(dicz1):
    a_group_role = dicz1.group("entities").filter_role("core")
    assert a_group_role.nlines ==  3
