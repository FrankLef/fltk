"""Dic abstract class."""

from abc import ABC
import re
from pathlib import Path
import pandas as pd
from typing import Final, Any
from enum import StrEnum, auto

type dic_lines = list[dict[str, Any]]
type dic_output = dict[str, Any] | list[dict[str, Any]]
type dic_names = str | list[str]


class AttrName(StrEnum):
    GROUP = auto()
    NAME = auto()
    SKIPPED = auto()
    ROLE = auto()
    RULE = auto()


class IDic(ABC):
    def __init__(self, name: str):
        self._name: str = name
        self._lines: dic_lines = []

    @property
    def name(self):
        return self._name

    @property
    def lines(self):
        return self._lines

    def load_xl(self, path: Path, sheet_nm: str) -> None:
        """Read an excel file containing the data to load into dic."""

        VARS_DTYPE: Final[dict[str, Any]] = {
            AttrName.GROUP.value: str,
            AttrName.NAME.value: str,
            AttrName.SKIPPED.value: bool,
            AttrName.ROLE.value: str,
            AttrName.RULE.value: str,
        }

        # NOTE: Important to specify the dtypes for excel.
        # Otherwise problem, e.g. with the activ field which will not be interpreted as boolean

        data = pd.read_excel(io=path, sheet_name=sheet_nm, dtype=VARS_DTYPE)
        msg = f"The excel data for dic '{self.name}' is empty."
        assert not data.empty, msg

        is_subset = set(VARS_DTYPE.keys()).issubset(data.columns)
        if not is_subset:
            msg = f"Required column names for dic '{self.name}' are missing."
            raise ValueError(msg)

        EMPTY_STR: Final[str] = ""
        # NOTE: Remove NaN put by pandas. Not sure this is necessary anymore since using xl_dtypes above.  Keep it.
        for var in VARS_DTYPE.keys():
            data[var] = data[var].fillna(EMPTY_STR)

        the_lines: dic_lines = data.to_dict(orient="records")
        the_lines = self.filter_skipped(the_lines)
        self._lines = the_lines

    def filter_skipped(self, lines: dic_lines) -> dic_lines:
        the_lines = list(
            filter(lambda line: not bool(line[AttrName.SKIPPED.value]), lines)
        )
        return the_lines

    def get_by_group(self, group: str | None = None) -> dic_lines:
        if group is not None:
            filtered_lines = list(
                filter(lambda line: line[AttrName.GROUP.value] == group, self._lines)
            )
        else:
            return self._lines
        if not len(filtered_lines):
            raise KeyError(f"No line found with group '{group}'.")
        return filtered_lines

    def get_attributes(
        self,
        names: list[str],
        attr: str,
        group: str | None = None,
        keep_list: bool = False,
    ) -> dic_output:
        NAME: Final[str] = AttrName.NAME.value

        the_lines = self.get_by_group(group)

        out: dic_lines = [
            {line[NAME]: line[attr]} for line in the_lines if line[NAME] in names
        ]
        if not len(out):
            msg: str = f"No '{attr}' attribute available for '{names}'."
            raise KeyError(msg)
        if not keep_list and len(out) == 1:
            return out[0]
        return out

    def match_tag(self, tag: str, text: str) -> bool:
        a_match = re.search(pattern=rf"\b{text}\b", string=tag)
        return a_match is not None

    def get_names_by_attr(
        self, value: str, attr: str, group: str | None = None, keep_list: bool = False
    ) -> dic_names:
        NAME: Final[str] = AttrName.NAME.value

        the_lines = self.get_by_group(group)

        out: dic_names = [
            line[NAME]
            for line in the_lines
            if self.match_tag(tag=line[attr], text=value)
        ]

        if not len(out):
            msg: str = f"No item found with {attr} = '{value}' in '{group}'."
            raise KeyError(msg)
        if not keep_list and len(out) == 1:
            return out[0]
        return out

    def get_by_role(
        self, role: str, group: str | None = None, keep_list: bool = False
    ) -> dic_names:
        out = self.get_names_by_attr(
            value=role, attr=AttrName.ROLE.value, group=group, keep_list=keep_list
        )
        return out

    def get_by_rule(
        self, rule: str, group: str | None = None, keep_list: bool = False
    ) -> dic_names:
        out = self.get_names_by_attr(
            value=rule, attr=AttrName.RULE.value, group=group, keep_list=keep_list
        )
        return out
