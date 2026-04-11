from typing import Any, Self
import re


class StrName(str):
    """Name must be non-empty and have valid characters."""

    def __new__(cls, value: Any) -> Self:
        val = str(value)
        val = val.replace(" ", "")
        if not val:
            raise ValueError("Empty name not allowed.")
        check = re.search(r"\W", string=val, flags=re.IGNORECASE)
        if check:
            raise ValueError(f"'{val}' not an allowed name.")
        return super().__new__(cls, val)
