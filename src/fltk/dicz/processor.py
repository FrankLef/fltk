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
        # the_lines = self.lines(line_nms)
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
