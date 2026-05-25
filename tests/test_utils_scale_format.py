import pytest
import fltk.utils.scale_format as sc


@pytest.mark.parametrize(
    "value, scale, fmt_str, expected",
    [
        [123456, 1e-3, "{:,.2f}$", "123.46$"],
        [0.123456, 100, "{:,.0f}%", "12%"],
        [123.456789, 1, "{:,.3f}", "123.457"],
    ],
)
def test_scale_format(value, scale, fmt_str, expected):
    """test with usual fmt_str."""
    formatted_val = sc.scale_format(value, scale=scale, fmt_str=fmt_str)
    assert formatted_val == expected


@pytest.mark.parametrize(
    "value, scale, digits, expected",
    [
        [123456, 1e-3, 2, "123.46 M"],
        [0.123456, 100, 3, "12.346 M"],
        [123.456789, 1, 1, "123.5 M"],
    ],
)
def test_scale_format_digits(value, scale, digits, expected):
    """test with digits."""
    fmt_str = f"{{:.{digits}f}} M"
    formatted_val = sc.scale_format(value, scale=scale, fmt_str=fmt_str)
    assert formatted_val == expected
