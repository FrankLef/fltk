import pytest

from fltk.dicz.group import DiczGroup


@pytest.fixture
def a_group(dicz1) -> DiczGroup:
    a_group = dicz1.bag("groups").group("entities")
    return a_group


def test_filter_role(a_group):
    new_group = a_group.filter_role("core")
    assert new_group.nlines == 2


def test_filter_rule(a_group):
    new_group = a_group.filter_rule("rule1")
    assert new_group.nlines == 2
