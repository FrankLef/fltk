import pytest


from fltk.specs.specs_group import SpecsGroup


@pytest.fixture
def a_group(mastr1) -> SpecsGroup:
    a_group = mastr1.specs("groups").group("entities")
    return a_group


def test_err_key(mastr1):
    with pytest.raises(KeyError):
        mastr1.specs("groups").group("X")


def test_line_nms(a_group):
    expected = ("CieA", "CieB", "CieC", "CieE", "CieF")
    assert a_group.line_nms == expected


def test_nlines(a_group):
    assert a_group.nlines == 5
