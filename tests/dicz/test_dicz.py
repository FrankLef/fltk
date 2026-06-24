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

class EntitiesNms(NamedTuple):
    group: str
    CieA: str
    CieB: str
    CieC: str
    CieE: str
    CieF: str

@pytest.fixture
def entities_nms():
    entities_nms=EntitiesNms(
        group="entities",
        CieA="CieA",
        CieB="CieB",
        CieC="CieC",
        CieE="CieE",
        CieF="CieF"
    )
    return entities_nms
    
def test_names_tupl(dicz1, entities_nms):
    a_group = dicz1.group("entities")
    names_tupl = a_group.names_tupl
    assert names_tupl==entities_nms
