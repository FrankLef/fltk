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


# def test_nbag(dicz1):
#     a_bag = dicz1.bag("groups")
#     assert a_bag.ngroups == 2
#     assert a_bag.nlines == 18


# def test_bags(dicz1, xlfile, xlsheet):
#     a_dicz = dicz1.bags(("groups", "xbr"))
#     assert isinstance(a_dicz, Dicz)
#     assert a_dicz.nbags == 2


def test_err_key(dicz1):
    with pytest.raises(KeyError):
        dicz1.bag("X")


# def test_bag_group(dicz1):
#     a_group = dicz1.bag("groups").group("entities")
#     assert a_group.nlines == 5


# def test_lines_value(dicz1):
#     a_group = dicz1.bag("groups").group("concepts")
#     line_keys = ("SalesNet", "MaterialCosts", "AssetsNongoodwillNoncash")
#     values = a_group.lines_value(line_keys=line_keys, item_nm="color")
#     assert len(values) == len(line_keys)
