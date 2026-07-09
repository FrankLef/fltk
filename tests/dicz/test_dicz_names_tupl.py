"""Test the dic class."""

import pytest
from pathlib import Path
import polars as pl
from typing import NamedTuple

from fltk.dicz.main import Dicz


@pytest.fixture
def dicz():
    return Dicz(key="dicz_test")


@pytest.fixture
def path():
    return Path(__file__).parent.joinpath("fixtures")


@pytest.fixture
def xlfile(path):
    return path.joinpath("bag_xbr.xlsx")


@pytest.fixture
def xlsheet():
    return "data"


@pytest.fixture
def dicz1(dicz, xlfile, xlsheet):
    df = pl.read_excel(xlfile, sheet_name=xlsheet)
    dicz.append(key="xbr", data=df)
    return dicz


def test_bag(dicz1, xlfile, xlsheet):
    a_bag = dicz1.bag("xbr")
    assert a_bag.ngroups == 3
    assert a_bag.nlines == 20


def test_group(dicz1):
    a_group = dicz1.bag("xbr").group("xbr_concepts")
    assert a_group.nlines == 12


class FsTypeNms(NamedTuple):
    name: str
    fstype: str
    fstype_lbl: str
    fstype_en: str
    fstype_fr: str


@pytest.fixture
def fstype_nms():
    fstype_nms = FsTypeNms(
        name="xbr_fstypes",
        fstype="fstype",
        fstype_lbl="fstype_lbl",
        fstype_en="fstype_en",
        fstype_fr="fstype_fr",
    )
    return fstype_nms


def test_names_tupl(dicz1, fstype_nms):
    a_group = dicz1.bag("xbr").group("xbr_fstypes")
    names_tupl = a_group.names_tupl
    assert names_tupl == fstype_nms
    assert names_tupl._fields == fstype_nms._fields
