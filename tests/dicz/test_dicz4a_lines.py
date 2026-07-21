import pytest


from fltk.dicz.group import DiczGroup
from fltk.dicz.processor import DiczProcessor


@pytest.fixture
def a_group(dicz1) -> DiczGroup:
    a_group = dicz1.bag("groups").group("entities")
    return a_group


def test_lines(a_group) -> None:
    a_proc = a_group.lines(("CieA", "CieB"))
    a_coll = a_proc.coll
    assert type(a_proc) is DiczProcessor
    assert len(a_coll) == 2


def test_get_names(a_group) -> None:
    the_names = a_group.lines(("CieA", "CieB")).get_names()
    assert the_names == ("CieA", "CieB")


def test_get_value_one(a_group) -> None:
    a_color = a_group.lines(("CieA",)).get_value("color")
    assert a_color == "magenta"


def test_get_value_many(a_group) -> None:
    the_colors = a_group.lines(("CieA", "CieC")).get_value("color")
    assert the_colors == {"CieA": "magenta", "CieC": "purple"}


def test_get_values(a_group) -> None:
    the_values = a_group.lines(("CieA", "CieC")).get_values()
    assert len(the_values) == 2


def test_filter_role(a_group) -> None:
    new_lines = a_group.lines().filter_role("core")
    new_coll = new_lines.coll
    assert type(new_lines) is DiczProcessor
    assert list(new_coll.keys()) == ["CieA", "CieB"]
    assert len(new_coll["CieA"].items()) == 7
    assert len(new_coll["CieB"].items()) == 7
    assert new_coll["CieA"].item("color").value == "magenta"


def test_filter_rule(a_group) -> None:
    new_lines = a_group.lines().filter_rule("rule1")
    new_coll = new_lines.coll
    assert type(new_lines) is DiczProcessor
    assert list(new_coll.keys()) == ["CieB", "CieC"]
    assert len(new_coll["CieB"].items()) == 7
    assert len(new_coll["CieC"].items()) == 7
    assert new_coll["CieC"].item("color").value == "purple"


def test_filter_role_value(a_group) -> None:
    the_colors = a_group.lines().filter_role("core").get_value("color")
    assert the_colors == {"CieA": "magenta", "CieB": "dodgerblue"}


def test_filter_role_names(a_group) -> None:
    the_names = a_group.lines().filter_role("core").get_names()
    assert the_names == ("CieA", "CieB")


def test_filter_rule_value(a_group) -> None:
    the_colors = a_group.lines().filter_rule("rule1").get_value("color")
    assert the_colors == {"CieB": "dodgerblue", "CieC": "purple"}


def test_filter_rule_names(a_group) -> None:
    the_names = a_group.lines().filter_rule("rule1").get_names()
    assert the_names == ("CieB", "CieC")
