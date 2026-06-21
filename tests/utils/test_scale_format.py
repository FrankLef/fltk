import pytest
import fltk.utils.format_scale as fmt


@pytest.mark.parametrize(
    "value, scale, mask, expected",
    [
        [123456, 1e-3, "{:,.2f}$", "123.46$"],
        [0.123456, 100, "{:,.0f}%", "12%"],
        [123.456789, 1, "{:,.3f}", "123.457"],
        [None, 1, "{:,.2f}$", "-"],
    ],
)
def test_format_scale(value, scale, mask, expected):
    """test with usual fmt_str."""
    formatted_val = fmt.format_scale(value, scale=scale, mask=mask)
    assert formatted_val == expected


@pytest.mark.parametrize(
    "value, scale, digits, expected",
    [
        [123456, 1e-3, 2, "123.46 $"],
        [0.123456, 100, 3, "12.346 $"],
        [123.456789, 1, 1, "123.5 $"],
    ],
)
def test_format_scale_digits(value, scale, digits, expected):
    """test with digits."""
    mask = f"{{:.{digits}f}} $"
    formatted_val = fmt.format_scale(value, scale=scale, mask=mask)
    assert formatted_val == expected
