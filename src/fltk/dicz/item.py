from dataclasses import dataclass
from re import search as re_search
from typing import Any


@dataclass
class DiczItem:
    key: str
    value: str

    def is_matched(self, pattern: str) -> bool:
        a_match = re_search(pattern=rf"\b{pattern}\b", string=str(self.value))
        return a_match is not None

    def split_tag(
        self, default: dict[str, Any], na: str = "_na", sep1: str = "~", sep2: str = "="
    ) -> dict[str, str] | None:
        # NOTE: Must use a special separator not a comma because commas are found in sub text. e.g. mask="{:,.2f}"
        tag_text: str | None = self.value

        if tag_text is None:
            return None

        if tag_text == na:
            return default

        is_tag = sep2 in tag_text
        if is_tag:
            try:
                tags = dict(item.split(sep2) for item in tag_text.split(sep1))
            except ValueError:
                return None
        else:
            return None
        return tags
