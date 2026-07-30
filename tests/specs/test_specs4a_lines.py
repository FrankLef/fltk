import pytest


from fltk.specs.specs_group import SpecsGroup
from fltk.specs.processor import SpecsProcessor


@pytest.fixture
def a_group(mastr1) -> SpecsGroup:
    a_group = mastr1.specs("groups").group("entities")
    return a_group


def test_lines_one(a_group) -> None:
    a_proc = a_group.lines("CieA")
    assert isinstance(a_proc, SpecsProcessor)
    assert a_proc.df.shape == (1, 9)


def test_lines_many(a_group) -> None:
    a_proc = a_group.lines(("CieA", "CieB"))
    assert isinstance(a_proc, SpecsProcessor)
    assert a_proc.df.shape == (2, 9)


def test_line_nms(a_group) -> None:
    line_nms = a_group.lines(("CieA", "CieB")).line_nms
    assert line_nms == ("CieA", "CieB")


def test_nlines(a_group) -> None:
    nlines = a_group.lines(("CieA", "CieB")).nlines
    assert nlines == 2
