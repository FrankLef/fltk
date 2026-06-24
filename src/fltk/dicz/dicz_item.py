from dataclasses import dataclass
import re


@dataclass
class DiczItem:
    key: str
    value: str

    def is_matched(self, pattern: str) -> bool:
        a_match = re.search(pattern=rf"\b{pattern}\b", string=self.value)
        return a_match is not None
    
    def split_tag(self, sep1: str = "~", sep2: str = "=") -> dict[str, str] | None:
        tag_text: str = self.value
        if tag_text is None:
            return None
        is_tag = (sep2 in tag_text)
        if is_tag:
            # NOTE: Must use a special separator not a comma because commas are found in sub text. e.g. mask="{:,.2f}"
            try:
                tags = dict(item.split(sep2) for item in tag_text.split(sep1))
            except ValueError:
                return None
        else:
            return None
        return tags
