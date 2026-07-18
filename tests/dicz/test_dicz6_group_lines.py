import pytest

from fltk.dicz.group import DiczGroup


@pytest.fixture
def a_group(dicz1) -> DiczGroup:
    a_group = dicz1.bag("groups").group("entities")
    return a_group


def test_lines_value_all(a_group):
    expected = {
        "CieA": "magenta",
        "CieB": "dodgerblue",
        "CieC": "purple",
        "CieE": "blue",
        "CieF": "black",
    }
    out = a_group.lines_value(line_nms=None, item_nm="color")
    assert out == expected


def test_lines_value_some(a_group):
    expected = {
        "CieA": "magenta",
        "CieB": "dodgerblue",
    }
    line_nms = ["CieA", "CieB"]
    out = a_group.lines_value(line_nms=line_nms, item_nm="color")
    assert out == expected


def test_lines_tag(a_group):
    default = {"scale": 1, "mask": "{:,.2f}"}
    expected = {
        "CieA": {"scale": "0.000001", "mask": "{:,.1f} M$"},
    }
    out = a_group.lines_tag(line_nms=["CieA"], item_nm="TsFmt", default=default)
    assert out == expected
