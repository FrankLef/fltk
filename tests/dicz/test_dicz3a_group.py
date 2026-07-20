import pytest


from fltk.dicz.group import DiczGroup


@pytest.fixture
def a_group(dicz1) -> DiczGroup:
    a_group = dicz1.bag("groups").group("entities")
    return a_group


def test_info(a_group):
    expected = {"nlines": 5, "nitems": 35}
    assert a_group.info == expected


def test_coll_one(a_group):
    a_coll = a_group.lines(("CieA", "CieB")).coll
    assert len(a_coll) == 2


def test_err_key(a_group):
    with pytest.raises(KeyError):
        a_group.lines("X")
