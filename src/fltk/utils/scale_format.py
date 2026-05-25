"""Multiplies a value by scale and formats it as a string."""


def scale_format(val: float, scale: float, fmt_str: str) -> str:
    """Multiplies a value by scale and formats it as a string.

    Very useful function used primarily in pandas when formating columns. See example below.

    Args:
        val (float): Value to format.
        scale (float): Scale used to multiply val.
        fmt_str (str): Format string used to format the scaled value.

    Examples:

    >>> df['new'] = df['val'].apply(scale_format, scale=1, fmt_str="{:,.2f}")  # doctest: +SKIP

    Returns:
        str: Scaled and formatted value.
    """
    scaled_val = val * scale
    formatted_val = fmt_str.format(scaled_val)
    return formatted_val
