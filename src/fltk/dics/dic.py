"""Dic abstract class."""

from abc import ABC
import re
from pathlib import Path
import pandas as pd
from typing import NamedTuple, Iterable, Final, Any
from enum import StrEnum, auto

type dic_lines = list[NamedTuple]
type dic_output = NamedTuple | list[NamedTuple]
type dic_names = str | list[str]
type dic_attrs = list[dict[str, Any]]


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

    @property
    def nlines(self):
        return len(self._lines)

    def load_data(
        self, path: Path, sheet_nm: str | None = None, is_xl: bool = True
    ) -> None:
        VARS_DTYPE: Final[dict[str, Any]] = {
            AttrName.GROUP: str,
            AttrName.NAME: str,
            AttrName.SKIPPED: bool,
            AttrName.ROLE: str,
            AttrName.RULE: str,
        }

        # NOTE: Important to specify the dtypes.
        # Otherwise problem, e.g. with the 'skipped' field which will not be interpreted as boolean.

        if is_xl:
            data = pd.read_excel(path, sheet_name=sheet_nm, dtype=VARS_DTYPE)
        else:
            data = pd.read_csv(path, dtype=VARS_DTYPE)

        if data.empty:
            raise ValueError(f"The import file '{path.name}' is empty.")

        is_subset = set(VARS_DTYPE.keys()).issubset(data.columns)
        if not is_subset:
            msg: str = f"Required column names in '{path.name}' are missing."
            raise ValueError(msg)

        EMPTY_STR: Final[str] = ""
        # NOTE: Remove NaN put by pandas. Not sure this is necessary anymore since using xl_dtypes above.  Keep it.
        for var in VARS_DTYPE.keys():
            data[var] = data[var].fillna(EMPTY_STR)

        lines: dic_lines = []
        for row in data.itertuples(index=False):
            lines.append(row)

        lines = self.filter_skipped(lines)

        self._lines = lines

    def load_csv(self, path: Path) -> None:
        self.load_data(path, is_xl=False)

    def load_xl(self, path: Path, sheet_nm: str) -> None:
        self.load_data(path, sheet_nm=sheet_nm)

    def filter_skipped(self, lines: dic_lines) -> dic_lines:
        the_lines: dic_lines = [line for line in lines if not line.skipped]  # type: ignore[attr-defined]
        return the_lines

    def get_by_group(self, group: str | None = None) -> dic_lines:
        if group is not None:
            the_lines: dic_lines = [line for line in self._lines if line.group == group]  # type: ignore[attr-defined]
        else:
            return self._lines
        if not len(the_lines):
            msg: str = f"No line found for group '{group}' in dic '{self._name}'."
            raise KeyError(msg)
        return the_lines

    def get_by_names(
        self, names: Iterable[str], group: str | None = None, keep_list: bool = False
    ) -> dic_output:
        group_lines = self.get_by_group(group)

        lines: dic_output = [line for line in group_lines if line.name in names]  # type: ignore[attr-defined]
        if not len(lines):
            msg: str = "No line found."
            raise KeyError(msg)
        if not keep_list and len(lines) == 1:
            return lines[0]
        return lines

    def match_tag(self, tag: str, text: str) -> bool:
        a_match = re.search(pattern=rf"\b{text}\b", string=tag)
        return a_match is not None

    def get_names_by_role(
        self, role: str, group: str | None = None, keep_list: bool = False
    ) -> dic_names:
        group_lines = self.get_by_group(group)

        names: dic_names = [
            line.name  # type: ignore[attr-defined]
            for line in group_lines
            if self.match_tag(tag=line.role, text=role)  # type: ignore[attr-defined]
        ]

        if not len(names):
            msg: str = f"No item found with role '{role}' in '{group}'."
            raise KeyError(msg)

        if not keep_list and len(names) == 1:
            return names[0]

        return names

    def get_names_by_rule(
        self, rule: str, group: str | None = None, keep_list: bool = False
    ) -> dic_names:
        group_lines = self.get_by_group(group)

        names: dic_names = [
            line.name  # type: ignore[attr-defined]
            for line in group_lines
            if self.match_tag(tag=line.rule, text=rule)  # type: ignore[attr-defined]
        ]

        if not len(names):
            msg: str = f"No item found with rule '{rule}' in '{group}'."
            raise KeyError(msg)

        if not keep_list and len(names) == 1:
            return names[0]

        return names

    def get_lines_by_role(
        self, role: str, group: str | None = None, keep_list: bool = False
    ) -> dic_output:
        # NOTE: The names must be in a list. i.e. keep_list=True
        names: list[str] = self.get_names_by_role(
            role=role, group=group, keep_list=True
        )  # type: ignore
        lines: dic_output = self.get_by_names(
            names=names, group=group, keep_list=keep_list
        )
        return lines

    def get_lines_by_rule(
        self, rule: str, group: str | None = None, keep_list: bool = False
    ) -> dic_output:
        # NOTE: The names must be in a list. i.e. keep_list=True
        names: list[str] = self.get_names_by_rule(
            rule=rule, group=group, keep_list=True
        )  # type: ignore
        lines: dic_output = self.get_by_names(
            names=names, group=group, keep_list=keep_list
        )
        return lines

    def get_tags(self, tag_text: str | None) -> dict[str, Any] | None:
        if tag_text is not None:
            try:
                tags = dict(item.split("=") for item in tag_text.split(","))
                # fields=[(field, str) for field in tags.keys()]
                # AttrTag = NamedTuple('AttrTag', fields)
                # print("tag_values:", tags.values())
                # raise KeyboardInterrupt()
                # attr_tag = AttrTag(tags.values())
            except ValueError:
                return None
        else:
            return None
        return tags

    def get_attributes(
        self, names: Iterable[str] | None, group: str, attr_nm: str
    ) -> dic_attrs:
        if names is not None:
            lines = self.get_by_names(names=names, group=group, keep_list=True)
        else:
            lines = self.get_by_group(group=group)
        attrs = []
        for line in lines:
            # NOTE: Must next to get the element of the iterator.
            attr_text = getattr(line, attr_nm)
            attr_dict = {line.name: attr_text}  # type: ignore[union-attr]
            attrs.append(attr_dict)
        return attrs
    
    def get_attributes_default(self,tag_text: str, default:Any, na:str="_na"):
        if tag_text != na:
            attr_dict = self.get_tags(tag_text)
        else:
            attr_dict = default
        return attr_dict
