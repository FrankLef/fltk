"""Test the dic class."""

import pytest
from pathlib import Path
import pandas as pd
from typing import NamedTuple

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


class EntitiesNms(NamedTuple):
    name: str
    CieA: str
    CieB: str
    CieC: str
    CieE: str
    CieF: str


@pytest.fixture
def entities_nms():
    entities_nms = EntitiesNms(
        name="entities",
        CieA="CieA",
        CieB="CieB",
        CieC="CieC",
        CieE="CieE",
        CieF="CieF",
    )
    return entities_nms


def test_names_tupl(dicz1, entities_nms):
    a_group = dicz1.bag("bag1").group("entities")
    names_tupl = a_group.names_tupl
    assert names_tupl == entities_nms
    assert names_tupl._fields == entities_nms._fields
