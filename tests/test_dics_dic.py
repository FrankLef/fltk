"""Test the log1ps module."""

import pytest
from pathlib import Path
import fltk.dics.dic as dc


class DicTest(dc.IDic):
    pass

@pytest.fixture
def dic():
    # dic = DicTest(name="dic_test")
    return DicTest(name="dic_test")

@pytest.fixture
def path():
    path =Path(__file__).parent.joinpath("fixtures", "ddict1.xlsx")
    return path

@pytest.fixture
def sheet():
    return "data"

def test_dic(dic):
    assert isinstance(dic, dc.IDic)
    
def test_name(dic):
    assert dic.name == "dic_test"

def test_load_xl(dic, path, sheet):
    dic.load_xl(path=path, sheet_nm=sheet)
    lines=dic.lines
    assert len(lines) == 18
    
@pytest.fixture
def loaded_dic(dic, path, sheet):
    dic.load_xl(path=path, sheet_nm=sheet)
    return dic

@pytest.mark.parametrize(
    "group, expected",
    [
        [None, 18],
        ["trialbal", 7],
        ["summ", 11],
    ],
)
def test_get_by_group(loaded_dic, group, expected):
    lines=loaded_dic.get_by_group(group=group)
    assert len(lines)==expected

@pytest.mark.parametrize(
    "names, attr, group, keep_list, expected",
    [
        [["fin_qrtr_tag"], "dtype", "trialbal", True, 
         [{"fin_qrtr_tag": "VARCHAR(10)"}]],
        [["concept", "fstype"], "dtype", "summ", True, 
         [{"concept": "VARCHAR"}, {"fstype": "VARCHAR"}]],
        [["fin_qrtr_tag"], "dtype", "trialbal", False, 
         {"fin_qrtr_tag": "VARCHAR(10)"}],
    ],
)   
def test_get_attributes(loaded_dic, names, attr, group, keep_list, expected):
    lines = loaded_dic.get_attributes(names=names, attr=attr, group=group, keep_list=keep_list)
    assert lines==expected