"""Test the dic class."""

import pytest
from pathlib import Path
import fltk.dic.main as dc
from fltk.dic.get_lines_names import match_params


class DicTest(dc.IDic):
    pass


@pytest.fixture
def dic():
    return DicTest(name="dic_test")


@pytest.fixture
def path():
    return Path(__file__).parent


@pytest.fixture
def xlfile(path):
    return path.joinpath("dic1.xlsx")


@pytest.fixture
def csvfile(path):
    return path.joinpath("dic1.csv")


@pytest.fixture
def sheet():
    return "data"


def test_dic(dic):
    assert isinstance(dic, dc.IDic)


def test_name(dic):
    assert dic.name == "dic_test"


def test_load_csv(dic, csvfile, sheet):
    dic.load_csv(path=csvfile)
    lines = dic.lines
    assert len(lines) == 18


def test_load_xl(dic, xlfile, sheet):
    dic.load_xl(path=xlfile, sheet_nm=sheet)
    lines = dic.lines
    assert len(lines) == 18


@pytest.fixture
def loaded_dic(dic, xlfile, sheet):
    dic.load_xl(path=xlfile, sheet_nm=sheet)
    return dic


def test_nlines(loaded_dic):
    assert loaded_dic.nlines == 18


@pytest.mark.parametrize(
    "group, expected",
    [
        [None, 18],
        ["trialbal", 7],
        ["summ", 11],
    ],
)
def test_get_lines_by_group(loaded_dic, group, expected):
    lines = loaded_dic.get_lines(group=group)
    assert len(lines) == expected


@pytest.mark.parametrize(
    "names, group, expected",
    [
        [["fin_qrtr_tag", "pertype", "fstype"], "trialbal", 3],
        [["fin_qrtr_tag"], "trialbal", 1],
    ],
)
def test_get_lines_by_names(loaded_dic, group, names, expected):
    lines = loaded_dic.get_lines_by_names(group=group, names=names)
    assert len(lines) == expected


@pytest.mark.parametrize(
    "dic_text, text, expected",
    [
        ["pk", "pk", True],
        ["pk,nn", "pk", True],
        ["pk,nn", "nn", True],
        ["pk,nn", "ren", False],
    ],
)
def test_match_tag(dic_text, text, expected):
    out = match_params(dic_text=dic_text, text=text)
    assert out == expected


@pytest.mark.parametrize(
    "group, role, expected",
    [
        ["trialbal", "ts", ("fin_qrtr_tag", "amt")],
        ["trialbal", "cat", ("entity",)],
        ["trialbal", "cat", ("entity",)],
    ],
)
def test_get_names_by_role(loaded_dic, group, role, expected):
    names = loaded_dic.get_names(group=group, role=role)
    assert names == expected


@pytest.mark.parametrize(
    "group, rule, expected",
    [
        ["trialbal", "nn", ("fstype", "amt")],
        ["trialbal", "ren", ("gl_no", "gl_desc")],
    ],
)
def test_get_names_by_rule(loaded_dic, group, rule, expected):
    names = loaded_dic.get_names(group=group, rule=rule)
    assert names == expected


def test_get_lines_err_group(loaded_dic):
    with pytest.raises(KeyError):
        loaded_dic.get_names(group="Error")


def test_get_lines_err_role(loaded_dic):
    with pytest.raises(AssertionError):
        loaded_dic.get_names(group="trialbal", role="Error")


@pytest.mark.parametrize(
    "tag_text, expected",
    [
        [None, None],
        ["_na", None],
        ["size=2~shape=dash", {"size": "2", "shape": "dash"}],
        [
            "scale=1~decimals=2~mask={:,.2f}",
            {"scale": "1", "decimals": "2", "mask": "{:,.2f}"},
        ],
    ],
)
def test_split_tag(loaded_dic, tag_text, expected):
    tags = loaded_dic.split_tag(tag_text)
    assert tags == expected


@pytest.mark.parametrize(
    "names, group, attr_nm, expected",
    [
        [["fstype"], "trialbal", "dtype", {"fstype": "VARCHAR(5)"}],
        [["pertype"], "trialbal", "LineGeom", {"pertype": "size=2,shape=dash"}],
        [
            ["pertype", "fstype"],
            "trialbal",
            "LineGeom",
            {"pertype": "size=2,shape=dash", "fstype": "size=2"},
        ],
    ],
)
def test_get_attributes(loaded_dic, names, group, attr_nm, expected):
    line = loaded_dic.get_attributes(names=names, group=group, attr_nm=attr_nm)
    assert line == expected
