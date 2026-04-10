from typing import Any, Self
import re

class StrName(str):
    """Name must be non-empty and have valid characters."""

    def __new__(cls, value: Any) -> Self:
        val = str(value)
        val = val.replace(" ", "")
        if not val:
            raise ValueError("Empty name.")
        if re.search(r"\W", val):
            raise ValueError(f"'{val}' is invalid for a name.")
        return super().__new__(cls, val)