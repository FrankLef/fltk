import pytest


from fltk.dicz.group import DiczGroup


@pytest.fixture
def a_group(dicz1) -> DiczGroup:
    a_group = dicz1.bag("groups").group("entities")
    return a_group


def test_info(a_group):
    expected = {"nlines": 5, "nitems": 35}
    assert a_group.info == expected


def test_line(a_group):
    a_line = a_group.line("CieA")
    assert a_line.nitems == 7


def test_err_key(a_group):
    with pytest.raises(KeyError):
        a_group.line("X")


def test_lines(a_group):
    the_lines = a_group.lines(("CieA", "CieB"))
    assert len(the_lines) == 2
