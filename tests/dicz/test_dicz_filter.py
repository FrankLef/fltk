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
    return path.joinpath("bag1.xlsx")


@pytest.fixture
def xlsheet():
    return "data1"


@pytest.fixture
def dicz1(dicz, xlfile, xlsheet):
    df = pd.read_excel(xlfile, sheet_name=xlsheet)
    dicz.append(key="bag1", data=df)
    return dicz


def test_bag(dicz1, xlfile, xlsheet):
    a_bag = dicz1.bag("bag1")
    assert a_bag.ngroups == 2
    assert a_bag.nlines == 18


def test_group(dicz1):
    a_group = dicz1.bag("bag1").group("entities")
    assert a_group.nlines == 5


def test_bag_filter(dicz1):
    a_bag = dicz1.bag("bag1")
    group_nms = ("entities",)
    filtered_bag = a_bag.filter(group_nms=group_nms)
    assert filtered_bag.ngroups == 1


def test_group_filter(dicz1):
    a_group = dicz1.bag("bag1").group("entities")
    line_nms = ("CieA", "CieB")
    filtered_group = a_group.filter(line_nms=line_nms)
    assert filtered_group.nlines == 2


def test_filter_role(dicz1):
    a_group_role = dicz1.bag("bag1").group("entities").filter_role("core")
    assert a_group_role.nlines == 3


def test_line_filter(dicz1):
    a_group = dicz1.bag("bag1").group("entities")
    item_nms = ("label", "color", "GtFmt")
    a_line = a_group.line("CieA").filter(item_nms=item_nms)
    assert a_line.nitems == 3
