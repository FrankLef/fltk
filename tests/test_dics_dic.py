"""Test the dic class."""

import pytest
from pathlib import Path
import fltk.dics.dic as dc


class DicTest(dc.IDic):
    pass


@pytest.fixture
def dic():
    return DicTest(name="dic_test")


@pytest.fixture
def path():
    return Path(__file__).parent.joinpath("fixtures")


@pytest.fixture
def xlfile(path):
    return path.joinpath("ddict1.xlsx")


@pytest.fixture
def csvfile(path):
    return path.joinpath("ddict1.csv")


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
def test_get_by_group(loaded_dic, group, expected):
    lines = loaded_dic.get_by_group(group=group)
    assert len(lines) == expected


@pytest.mark.parametrize(
    "names, group, keep_list, expected",
    [
        [["fin_qrtr_tag", "pertype", "fstype"], "trialbal", False, 3],
        [["fin_qrtr_tag"], "trialbal", True, 1],
    ],
)
def test_get_by_names(loaded_dic, names, group, keep_list, expected):
    lines = loaded_dic.get_by_names(names=names, group=group, keep_list=keep_list)
    assert len(lines) == expected


@pytest.mark.parametrize(
    "tag, text, expected",
    [
        ["pk", "pk", True],
        ["pk,nn", "pk", True],
        ["pk,nn", "nn", True],
        ["pk,nn", "ren", False],
    ],
)
def test_match_tag(dic, tag, text, expected):
    out = dic.match_tag(tag=tag, text=text)
    assert out == expected


@pytest.mark.parametrize(
    "role, group, keep_list, expected",
    [
        ["ts", "trialbal", False, ["fin_qrtr_tag", "amt"]],
        ["cat", "trialbal", False, "entity"],
        ["cat", "trialbal", True, ["entity"]],
    ],
)
def test_get_names_by_role(loaded_dic, role, group, keep_list, expected):
    names = loaded_dic.get_names_by_role(role=role, group=group, keep_list=keep_list)
    assert names == expected


@pytest.mark.parametrize(
    "rule, group, keep_list, expected",
    [
        ["nn", "trialbal", False, ["fstype", "amt"]],
        ["ren", "trialbal", False, ["gl_no", "gl_desc"]],
    ],
)
def test_get_names_by_rule(loaded_dic, rule, group, keep_list, expected):
    names = loaded_dic.get_names_by_rule(rule=rule, group=group, keep_list=keep_list)
    assert names == expected


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
def test_get_tags(loaded_dic, tag_text, expected):
    tags = loaded_dic.get_tags(tag_text)
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
