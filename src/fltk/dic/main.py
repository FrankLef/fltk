"""Dic abstract class."""

from abc import ABC

from pathlib import Path

from typing import NamedTuple, Iterable, Any
from enum import StrEnum, auto

from . import get_lines_names as gl

from . import dic_namedtuple as nt

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

    def __repr__(self) -> str:
        info: dict[str, Any] = {
            "name": self.name,
            "ngroups": str(self.ngroups),
            "nlines": str(self.nlines),
        }
        msg: str = "\n".join([key + ": " + val for key, val in info.items()])
        return msg

    @property
    def name(self):
        return self._name

    @property
    def groups(self) -> tuple[str, ...]:
        the_groups = [line.group for line in self._lines]  # type: ignore[attr-defined]
        # use dict, not set, to keep original order of groups
        groups = tuple(dict.fromkeys(the_groups))
        return groups

    @property
    def ngroups(self):
        return len(self.groups)

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

    def get_lines(
        self, group: str | None = None, role: str | None = None, rule: str | None = None
    ) -> dic_lines:
        the_lines = gl.get_lines(self._lines, group=group, role=role, rule=rule)
        return the_lines

    def get_names(
        self, group: str | None = None, role: str | None = None, rule: str | None = None
    ) -> tuple[str, ...]:
        the_names = gl.get_names(self._lines, group=group, role=role, rule=rule)
        return the_names

    def get_lines_by_names(self, group: str, names: Iterable[str] | None) -> dic_lines:
        the_lines = gl.get_lines_by_names(self._lines, group=group, names=names)
        return the_lines

    def get_namedtuple(self, group: str) -> Any:
        dic_named_tuple = nt.get_namedtuple(self._lines, group)

        return dic_named_tuple

    def get_attributes(
        self, group: str, names: Iterable[str] | None, attr_nm: str
    ) -> dict[Any, Any]:
        the_lines = self.get_lines_by_names(group=group, names=names)
        attrs = {line.name: getattr(line, attr_nm) for line in the_lines}  # type: ignore[attr-defined]
        return attrs

    def split_tag(self, tag_text: str | None, sep: str = "~") -> dict[str, Any] | None:
        """Split a tag into items of a dictionnary.

        Args:
            tag_text (str | None): The tag text.
            sep (str, optional): Separator of items in the tag text. Defaults to "~".

        Returns:
            dict[str, Any] | None: Dictionnary of tag items.
        """
        tags = dic_tags.split_tag(tag_text=tag_text, sep=sep)
        return tags

    def get_tags(
        self,
        group: str,
        names: Iterable[str] | None,
        attr_nm: str,
        default: dict[str, Any],
        na: str = "_na",
        sep: str = "~",
    ) -> dict[str, Any] | None:
        """Get a dictionnary of tags for each given name in a group.

        Args:
            group (str): Name of the group.
            names (Iterable[str] | None): Names within the group.
            attr_nm (str): Attribute name.
            default (dict[str, Any]): Default tag when `na` is the tag text.
            na (str, optional): NA value will return tag default. Defaults to "_na".
            sep (str, optional): Separator of items within the tag text. Cannot be a punctuation. Defaults to "~".

        Returns:
            dict[str, Any] | None: Dictionnary of tags.
        """
        attr_dict = dic_tags.get_tags(
            inst=self,
            group=group,
            names=names,
            attr_nm=attr_nm,
            default=default,
            na=na,
            sep=sep,
        )
        return attr_dict
