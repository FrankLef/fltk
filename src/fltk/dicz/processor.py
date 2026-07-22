from copy import deepcopy
from typing import Any

from .base import DiczNames, DiczVar as vars
from .line import DiczLines


class DiczProcessor:
    def __init__(self, coll: DiczLines):
        self.coll = coll

    def get_names(self) -> DiczNames:
        copied_coll = deepcopy(self.coll)

        names = tuple(copied_coll.keys())

        return names

    def get_value(self, item_nm: str) -> dict[str, Any] | Any:
        copied_coll = deepcopy(self.coll)

        the_values = {
            line_nm: val.value(item_nm) for line_nm, val in copied_coll.items()
        }
        if len(the_values) == 1:
            a_value = next(iter(the_values.values()))
            return a_value
        return the_values

    def get_values(self) -> dict[str, Any] | Any:
        copied_coll = deepcopy(self.coll)
        return copied_coll.values()

    @staticmethod
    def filter_pattern(coll: DiczLines, item_nm: str, pattern: str) -> DiczNames:
        """Filter the lines using the value of a given item.

        Args:
            item_nm (str): Name of the item.
            pattern (str): Pattern used to select the item.

        Returns:
            Self: DiczNames.
        """
        line_nms = tuple(
            key
            for key, val in coll.items()
            if val.is_matched(item_nm=item_nm, pattern=pattern)
        )
        return line_nms

    def filter_role(self, role: str) -> "DiczProcessor":
        copied_coll = deepcopy(self.coll)
        line_nms = self.filter_pattern(copied_coll, item_nm=vars.ROLE, pattern=role)
        filtered_coll = {line_nm: copied_coll[line_nm] for line_nm in line_nms}
        return DiczProcessor(filtered_coll)

    def filter_rule(self, rule: str) -> "DiczProcessor":
        copied_coll = deepcopy(self.coll)
        line_nms = self.filter_pattern(copied_coll, item_nm=vars.RULE, pattern=rule)
        filtered_coll = {line_nm: copied_coll[line_nm] for line_nm in line_nms}
        return DiczProcessor(filtered_coll)

    def get_tag(self, item_nm: str, default: dict[str, Any]) -> dict[str, Any] | Any:
        copied_coll = deepcopy(self.coll)

        the_tags = {
            line_nm: self.split_tag(tag_text=val.value(item_nm), default=default)
            for line_nm, val in copied_coll.items()
        }
        if len(the_tags) == 1:
            a_tag = next(iter(the_tags.values()))
            return a_tag
        return the_tags

    @staticmethod
    def split_tag(
        tag_text: str,
        default: dict[str, Any],
        na: str = "_na",
        sep1: str = "~",
        sep2: str = "=",
    ) -> dict[str, str] | None:
        # NOTE: Must use a special separator not a comma because commas are found in sub text. e.g. mask="{:,.2f}"

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
