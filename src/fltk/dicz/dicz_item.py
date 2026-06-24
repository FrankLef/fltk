from dataclasses import dataclass
import re


@dataclass
class DiczItem:
    key: str
    value: str

    def is_matched(self, pattern: str) -> bool:
        a_match = re.search(pattern=rf"\b{pattern}\b", string=self.value)
        return a_match is not None
