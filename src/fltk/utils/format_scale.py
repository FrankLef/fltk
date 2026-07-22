"""Multiplies a value by scale and formats it as a string."""

import polars as pl
from typing import Any, Final
# from ..dic.main import IDic


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
    is_ok: bool = value is not None
    if is_ok:
        scaled_val: float = value * scale
        formatted_val: str = mask.format(scaled_val)
    else:
        formatted_val = na
    return formatted_val


def format_scale_groups(
    data: pl.DataFrame,
    group_col: str,
    val_col: str,
    fmt_col: str,
    tags: dict[str, Any],
    default: dict[str, Any],
) -> pl.DataFrame:
    SCALE: Final[str] = "scale"
    MASK: Final[str] = "mask"

    a_scale: float = float(default[SCALE])
    a_mask: str = default[MASK]
    # Set the entire column to the default format.
    data = data.with_columns(
        pl.col(val_col)
        .map_elements(
            lambda v: format_scale(v, scale=a_scale, mask=a_mask),
            return_dtype=pl.String,
        )
        .alias(fmt_col)
    )

    for group_nm, tag in tags.items():
        a_scale = float(tag[SCALE])
        a_mask = tag[MASK]
        data = data.with_columns(
            pl.when(pl.col(group_col) == group_nm)
            .then(
                pl.col(val_col).map_elements(
                    lambda v: format_scale(v, scale=a_scale, mask=a_mask),
                    return_dtype=pl.String,
                )
            )
            .otherwise(pl.col(fmt_col))
            .alias(fmt_col)
        )

    return data
