"""Dic abstract class."""

from abc import ABC
import re
from pathlib import Path
import pandas as pd
from typing import NamedTuple, Final, Any
from enum import StrEnum, auto

type dic_lines = list[NamedTuple]
type dic_output = NamedTuple | list[NamedTuple]
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

    @property
    def nlines(self):
        return len(self._lines)

    def load_xl(self, path: Path, sheet_nm: str) -> None:
        """Read an excel file containing the data to load into dic."""

        VARS_DTYPE: Final[dict[str, Any]] = {
            AttrName.GROUP: str,
            AttrName.NAME: str,
            AttrName.SKIPPED: bool,
            AttrName.ROLE: str,
            AttrName.RULE: str,
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
                
        lines:dic_lines=[]
        for row in data.itertuples(index=False):
            lines.append(row)
            
        lines = self.filter_skipped(lines)
        self._lines = lines

    def filter_skipped(self, lines: dic_lines) -> dic_lines:
        the_lines:dic_lines = [line for line in lines if not line.skipped]  # type: ignore[attr-defined]
        
        return the_lines

    def get_by_group(self, group: str | None = None) -> dic_lines:
        if group is not None:
            the_lines:dic_lines = [line for line in self._lines if line.group == group]  # type: ignore[attr-defined]
        else:
            return self._lines
        if not len(the_lines):
            msg:str = f"No line found for group '{group}' in dic 'self._name'."
            raise KeyError(msg)
        return the_lines

    def get_lines(
        self, names: list[str], group: str | None = None, keep_list: bool = False
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


    def get_by_role(
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

    def get_by_rule(
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
    
    def get_lines_by_role(self, role: str, group: str | None = None, keep_list: bool = False
    )->dic_output:
        # NOTE: The names must be in a list. i.e. keep_list=True
        names: list[str] = self.get_by_role(role=role, group=group, keep_list=True)  # type: ignore
        lines:dic_output=self.get_lines(names=names, group=group, keep_list=keep_list)
        return lines
    
    def get_lines_by_rule(self, rule: str, group: str | None = None, keep_list: bool = False
    )->dic_output:
        # NOTE: The names must be in a list. i.e. keep_list=True
        names: list[str] = self.get_by_rule(rule=rule, group=group, keep_list=True)  # type: ignore
        lines:dic_output=self.get_lines(names=names, group=group, keep_list=keep_list)
        return lines
