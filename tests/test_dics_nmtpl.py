"""Test the dic class."""

import pytest
from pathlib import Path
import fltk.dics.dic as dc


class DicTest(dc.IDic):
    pass


@pytest.fixture
def dic():
    return DicTest(name="dic_nmtpl")


@pytest.fixture
def path():
    return Path(__file__).parent.joinpath("fixtures")


@pytest.fixture
def xlfile(path):
    return path.joinpath("dic2.xlsx")


@pytest.fixture
def sheet():
    return "data"


def test_dic(dic):
    assert isinstance(dic, dc.IDic)


def test_name(dic):
    assert dic.name == "dic_nmtpl"


def test_load_xl(dic, xlfile, sheet):
    dic.load_xl(path=xlfile, sheet_nm=sheet)
    lines = dic.lines
    assert len(lines) == 17


@pytest.fixture
def loaded_dic(dic, xlfile, sheet):
    dic.load_xl(path=xlfile, sheet_nm=sheet)
    return dic


def test_get_nmtpl(loaded_dic):
    nmtpl = loaded_dic.get_namedtuple(group="trialbal")
    assert isinstance(nmtpl, tuple) and hasattr(nmtpl, "_fields")


def test_err_name(loaded_dic):
    with pytest.raises(KeyError):
        loaded_dic.get_namedtuple(group="err_name")


def test_err_duplicates(loaded_dic):
    with pytest.raises(KeyError):
        loaded_dic.get_namedtuple(group="err_dupl")
