import pytest
from typing import NamedTuple, Any

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


@pytest.fixture
def names_tupl() -> NamedTuple:
    class NamesTupl(NamedTuple):
        name: str = "entities"
        CieA: str = "CieA"
        CieB: str = "CieB"
        CieC: str = "CieC"
        CieE: str = "CieE"
        CieF: str = "CieF"

    return NamesTupl()


def test_names_tupl(a_group, names_tupl) -> None:
    assert a_group.names_tupl == names_tupl


@pytest.fixture
def group_one(mastr1) -> SpecsGroup:
    a_group = mastr1.specs("groups").group("fstypes")
    return a_group


@pytest.fixture
def names_tupl_one() -> NamedTuple:
    class NamesTupl(NamedTuple):
        name: str = "fstypes"
        ratios: str = "ratios"

    return NamesTupl()


def test_names_tupl_one(group_one, names_tupl_one) -> None:
    assert group_one.names_tupl == names_tupl_one


@pytest.fixture
def tags() -> dict[str, Any]:
    tags = {
        "CieA": {"size": 2, "shape": "dash"},
        "CieB": "_na",
        "CieC": {"size": 3, "shape": "dot"},
        "CieE": "_na",
        "CieF": "_na",
    }
    return tags


def test_rem_non_dicts(a_group, tags) -> None:
    clean_tags = a_group.rem_non_dicts(tags)
    expected = {
        "CieA": {"size": 2, "shape": "dash"},
        "CieC": {"size": 3, "shape": "dot"},
    }
    assert clean_tags == expected
