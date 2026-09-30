"""Test the log1ps module."""

import pytest
from fltk.utils.clean_str import clean_ws, clean_sql


@pytest.mark.parametrize(
    "text, expected",
    [
        ["\n A text *   to\ttest\r  \t", "A text * to test"],
        ["\n A\f text\t *   to\r  test\t", "A text * to test"],
        [" ", None],
        [" \n ", None],
        ["", None],
        [None, None],
    ],
)
def test_clean_ws(text, expected) -> None:
    out = clean_ws(text)
    assert out == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        [" \n SELECT *   \tFROM\r table \t ", "SELECT * FROM table;"],
        [";\n SELECT *   \tFROM\r table \t;", "SELECT * FROM table;"],
    ],
)
def test_clean_sql(text, expected) -> None:
    out = clean_sql(text)
    assert out == expected


def test_clean_sql_err() -> None:
    with pytest.raises(ValueError):
        clean_sql("")
