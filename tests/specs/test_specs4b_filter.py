import pytest


from fltk.specs.specs_group import SpecsGroup
from fltk.specs.processor import SpecsProcessor


@pytest.fixture
def a_group(mastr1) -> SpecsGroup:
    a_group = mastr1.specs("groups").group("entities")
    return a_group


def test_filter_role(a_group) -> None:
    new_lines = a_group.lines().filter_role("core")
    assert isinstance(new_lines, SpecsProcessor)
    assert new_lines.get_names() == ("CieA", "CieB")


def test_filter_rule(a_group) -> None:
    new_lines = a_group.lines().filter_rule("rule1")
    assert isinstance(new_lines, SpecsProcessor)
    assert new_lines.get_names() == ("CieB", "CieC")


def test_filter_role_value(a_group) -> None:
    the_values = a_group.lines().filter_role("core").get_value("color")
    assert the_values == {"CieA": "magenta", "CieB": "dodgerblue"}


def test_filter_rule_value(a_group) -> None:
    the_values = a_group.lines().filter_rule("rule1").get_value("color")
    assert the_values == {"CieB": "dodgerblue", "CieC": "purple"}
