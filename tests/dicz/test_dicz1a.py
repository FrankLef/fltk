import pytest
from fltk.dicz.bag import DiczBag


def test_info(dicz1):
    expected = {"nbags": 2}
    assert dicz1.info == expected


def test_bag(dicz1):
    a_bag = dicz1.bag("groups")
    assert isinstance(a_bag, DiczBag)


def test_bags(dicz1):
    the_bags = dicz1.bags()
    assert len(the_bags) == 2


def test_err_key(dicz1):
    with pytest.raises(KeyError):
        dicz1.bag("X")
