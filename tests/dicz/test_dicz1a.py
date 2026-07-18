import pytest
from fltk.dicz.main import Dicz
from fltk.dicz.bag import DiczBag


def test_info(dicz1):
    expected = {"nbags": 2}
    assert dicz1.info == expected


def test_bag(dicz1):
    a_bag = dicz1.bag("groups")
    assert isinstance(a_bag, DiczBag)


def test_bags(dicz1):
    a_dicz = dicz1.bags(["groups"])
    assert isinstance(a_dicz, Dicz)


def test_err_key(dicz1):
    with pytest.raises(KeyError):
        dicz1.bag("X")
