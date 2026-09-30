"""Test the log1ps module."""

import pytest
from fltk.utils.clean_ws import clean_ws


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
def test_clean_ws(text, expected):
    out = clean_ws(text)
    assert out == expected
