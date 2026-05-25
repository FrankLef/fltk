import pytest
import fltk.utils.scale_format as sc


@pytest.mark.parametrize(
    "val, scale, fmt_str, expected",
    [
        [123456, 1e-3, "{:,.2f}$", "123.46$"],
        [0.123456, 100, "{:,.0f}%", "12%"],
        [123.456789, 1, "{:,.3f}", "123.457"],
    ],
)
def test_scale_format(val, scale, fmt_str, expected):
    formatted_val = sc.scale_format(val, scale=scale, fmt_str=fmt_str)
    assert formatted_val == expected
