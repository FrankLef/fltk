import pytest


from fltk.specs.specs_group import SpecsGroup
from fltk.specs.processor import SpecsProcessor


@pytest.fixture
def a_group(mastr1) -> SpecsGroup:
    a_group = mastr1.specs("groups").group("entities")
    return a_group


def test_lines(a_group) -> None:
    a_proc = a_group.lines(("CieA", "CieB"))
    assert isinstance(a_proc, SpecsProcessor)


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
    the_values = a_group.lines(("CieA", "CieC")).get_values(item_nms=("label", "color"))
    assert len(the_values) == 2


def test_get_split_one(a_group) -> None:
    the_periods = a_group.lines(("CieA",)).get_split("periods")
    expected = ("q2021-4", "q2022-4", "q2023-4", "q2024-4", "q2025-4")
    assert the_periods == expected


def test_get_split_many(a_group) -> None:
    the_periods = a_group.lines(("CieA", "CieC")).get_split("periods")
    expected = {
        "CieA": ("q2021-4", "q2022-4", "q2023-4", "q2024-4", "q2025-4"),
        "CieC": ("q2021-4", "q2022-4", "q2023-4"),
    }
    assert the_periods == expected


def test_get_tag(a_group) -> None:
    default = {"size": "1", "shape": "solid"}
    a_tag = a_group.lines(("CieA",)).get_tag("LineGeom", default=default)
    expected = {"size": "2", "shape": "dash"}
    assert a_tag == expected


def test_get_many_tag(a_group) -> None:
    default = {"size": "1", "shape": "solid"}
    the_tags = a_group.lines(("CieA", "CieC")).get_tag("LineGeom", default=default)
    expected = {
        "CieA": {"size": "2", "shape": "dash"},
        "CieC": {"size": "3", "shape": "dot"},
    }
    assert the_tags == expected
