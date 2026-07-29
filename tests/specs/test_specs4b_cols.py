import pytest


from fltk.specs.specs_group import SpecsGroup


@pytest.fixture
def a_group(mastr1) -> SpecsGroup:
    a_group = mastr1.specs("groups").group("entities")
    return a_group


def test_lines_one_cols_one(a_group) -> None:
    out = a_group.lines("CieA").cols("color")
    expected = "magenta"
    assert out == expected


def test_lines_one_cols_many(a_group) -> None:
    out = a_group.lines("CieA").cols(("label", "color"))
    expected = {"label": "Consolidated", "color": "magenta"}
    assert out == expected


def test_lines_many_cols_one(a_group) -> None:
    out = a_group.lines(("CieA", "CieC")).cols("color")
    expected = {"CieA": "magenta", "CieC": "purple"}
    assert out == expected


def test_lines_many_cols_many(a_group) -> None:
    out = a_group.lines(("CieA", "CieC")).cols(("color", "label"))
    expected = {
        "CieA": {"color": "magenta", "label": "Consolidated"},
        "CieC": {"color": "purple", "label": "Mexico"},
    }
    assert out == expected


def test_lines_one_cols_one_eval_dict(a_group) -> None:
    out = a_group.lines("CieA").cols("geomLine", is_lit_eval=True)
    expected = {"size": 2, "shape": "dash"}
    assert out == expected


def test_lines_one_cols_one_eval_tupl(a_group) -> None:
    out = a_group.lines("CieA").cols("periods", is_lit_eval=True)
    expected = ("q2021-4", "q2022-4", "q2023-4", "q2024-4", "q2025-4")
    assert out == expected


def test_lines_many_cols_one_eval(a_group) -> None:
    out = a_group.lines(("CieA", "CieC")).cols("geomLine", is_lit_eval=True)
    expected = {
        "CieA": {"size": 2, "shape": "dash"},
        "CieC": {"size": 3, "shape": "dot"},
    }
    assert out == expected


def test_lines_one_cols_one_eval_na(a_group) -> None:
    out = a_group.lines("CieE").cols("geomLine", is_lit_eval=True)
    expected = "_na"
    assert out == expected


def test_lines_one_cols_one_eval_null(a_group) -> None:
    out = a_group.lines("CieF").cols("geomLine", is_lit_eval=True)
    assert out is None
