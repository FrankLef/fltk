import pytest

from fltk.dicz.group import DiczGroup


@pytest.fixture
def a_group(dicz1) -> DiczGroup:
    a_group = dicz1.bag("groups").group("entities")
    return a_group


def test_filter_role(a_group):
    the_lines = a_group.filter_role("core")
    assert len(the_lines) == 2


def test_filter_role_names(a_group):
    the_names = a_group.filter_role("core", names_only=True)
    assert the_names == ("CieA", "CieB")


def test_filter_rule(a_group):
    the_lines = a_group.filter_rule("rule1")
    assert len(the_lines) == 2


def test_filter_rule_names(a_group):
    the_names = a_group.filter_rule("rule1", names_only=True)
    assert the_names == ("CieB", "CieC")
