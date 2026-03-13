"""Dic abstract class."""

from abc import ABC
import re
from pathlib import Path

from typing import NamedTuple, Iterable, Any
from enum import StrEnum, auto

from . import dic_namedtuple as dic_nt
from . import dic_lines_names as dic_ln
from . import dic_tags
from . import dic_load

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
        lines = dic_load.load_data(self, path=path, sheet_nm=sheet_nm, is_xl=is_xl)
        self._lines = lines

    def load_csv(self, path: Path) -> None:
        self.load_data(path, is_xl=False)

    def load_xl(self, path: Path, sheet_nm: str) -> None:
        self.load_data(path, sheet_nm=sheet_nm)

    def filter_skipped(self, lines: dic_lines) -> dic_lines:
        the_lines: dic_lines = [line for line in lines if not line.skipped]  # type: ignore[attr-defined]
        return the_lines

    def get_namedtuple(self, group: str) -> Any:
        dic_named_tuple = dic_nt.get_namedtuple(self, group)
        return dic_named_tuple

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
        names = dic_ln.get_names_by_role(
            inst=self, role=role, group=group, keep_list=keep_list
        )
        return names

    def get_names_by_rule(
        self, rule: str, group: str | None = None, keep_list: bool = False
    ) -> dic_names:
        names = dic_ln.get_names_by_rule(
            inst=self, rule=rule, group=group, keep_list=keep_list
        )
        return names

    def get_lines_by_role(
        self, role: str, group: str | None = None, keep_list: bool = False
    ) -> dic_output:
        lines = dic_ln.get_lines_by_role(
            inst=self, role=role, group=group, keep_list=keep_list
        )
        return lines

    def get_lines_by_rule(
        self, rule: str, group: str | None = None, keep_list: bool = False
    ) -> dic_output:
        lines = dic_ln.get_lines_by_rule(
            inst=self, rule=rule, group=group, keep_list=keep_list
        )
        return lines

    def get_attributes(
        self, names: Iterable[str] | None, group: str, attr_nm: str
    ) -> dict[Any, Any]:
        if names is not None:
            lines = self.get_by_names(names=names, group=group, keep_list=True)
        else:
            lines = self.get_by_group(group=group)
        attrs = {line.name: getattr(line, attr_nm) for line in lines}  # type: ignore[union-attr]
        return attrs

    def get_tags(
        self, tag_text: str | None, sep: str = chr(126)
    ) -> dict[str, Any] | None:
        tags = dic_tags.get_tags(tag_text=tag_text, sep=sep)
        return tags

    def get_tags_default(
        self,
        names: Iterable[str] | None,
        group: str,
        attr_nm: str,
        default: dict[str, Any],
        na: str = "_na",
        sep: str = chr(126),
    ) -> dict[str, Any] | None:
        attr_dict = dic_tags.get_tags_default(
            inst=self,
            names=names,
            group=group,
            attr_nm=attr_nm,
            default=default,
            na=na,
            sep=sep,
        )
        return attr_dict
