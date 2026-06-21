"""Multiplies a value by scale and formats it as a string."""

import pandas as pd


def format_scale(value: float, scale: float, mask: str, na: str = "-") -> str:
    """Multiplies a value by scale and formats it as a string.

    Very useful function used primarily in pandas when formating columns for tables and plots. See example below.

    Args:
        value (float): Value to format.
        scale (float): Scale used to multiply val.
        mask (str): Format string used to format the scaled value.

    Examples:

    >>> df['new'] = df['val'].apply(scale_format, scale=1, mask="{:,.2f}")  # doctest: +SKIP

    Returns:
        str: Formatted value in a given scale.
    """
    is_ok: bool = not (pd.isna(value) | (value is None))
    if is_ok:
        scaled_val = value * scale
        formatted_val = mask.format(scaled_val)
    else:
        formatted_val = na
    return formatted_val
