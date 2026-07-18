import pytest

from fltk.dicz.group import DiczLine


@pytest.fixture
def a_line(dicz1) -> DiczLine:
    a_line = dicz1.bag("groups").group("entities").line("CieA")
    return a_line


def test_info(a_line):
    expected = {"nitems": 7}
    assert a_line.info == expected


def test_items(a_line):
    item_nms = ["label", "color"]
    the_items = a_line.items(item_nms)
    assert len(the_items) == 2


def test_value(a_line):
    value = a_line.value("color")
    assert value == "magenta"


def test_values(a_line):
    item_nms = ["label", "color"]
    values = a_line.values(item_nms)
    expected = {"label": "Consolidated", "color": "magenta"}
    assert values == expected
