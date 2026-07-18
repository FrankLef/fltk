import pytest


from fltk.dicz.bag import DiczBag


@pytest.fixture
def a_bag(dicz1) -> DiczBag:
    a_bag = dicz1.bag("groups")
    return a_bag


def test_info(a_bag):
    expected = {"ngroups": 2, "nlines": 18}
    assert a_bag.info == expected


def test_group(a_bag):
    a_group = a_bag.group("entities")
    assert a_group.nlines == 5


def test_err_key(a_bag):
    with pytest.raises(KeyError):
        a_bag.group("X")


def test_groups(a_bag):
    new_bag = a_bag.groups(("entities", "concepts"))
    assert isinstance(new_bag, DiczBag)
    assert new_bag.ngroups == 2
