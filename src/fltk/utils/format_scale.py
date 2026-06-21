"""Multiplies a value by scale and formats it as a string."""

import pandas as pd
from typing import Any, Final
from ..dic.main import IDic


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
        scaled_val: float = value * scale
        formatted_val: str = mask.format(scaled_val)
    else:
        formatted_val = na
    return formatted_val


def format_scale_with_dic(
    data: pd.DataFrame,
    dic: IDic,
    group: str,
    group_col: str,
    group_nms: dict[str, Any],
    val_col: str,
    fmt_col: str,
    attr_nm: str,
    default_fmt: dict[str, Any] = {"scale": 1, "mask": "{:,.2f}"},
) -> pd.DataFrame:
    SCALE: Final[str] = "scale"
    MASK: Final[str] = "mask"

    a_scale: float = float(default_fmt[SCALE])
    a_mask: str = default_fmt[MASK]
    data[fmt_col] = data[val_col].apply(format_scale, scale=a_scale, mask=a_mask)

    groups_attrs = dic.get_tags_default(
        group_nms,
        group=group,
        attr_nm=attr_nm,
        default=default_fmt,
    )

    # NOTE: Must use empty dict in (groups_attrs or {}) to avoid error message
    for group_nm, tag in (groups_attrs or {}).items():
        a_scale = float(tag[SCALE])
        a_mask = tag[MASK]
        # NOTE: Must use index like this to be able to use a loop in pandas!
        for index, row in data.iterrows():
            if row[group_col] == group_nm:
                formatted_value = format_scale(
                    data.at[index, val_col], scale=a_scale, mask=a_mask
                )
                data.at[index, fmt_col] = formatted_value
    return data
