"""Dic abstract class."""

from abc import ABC
import re
from pathlib import Path
import pandas as pd
from typing import Final, Any
from enum import Enum

type dic_output = dict[str, Any] | list[dict[str, Any]]

class AttrType(Enum):
    ROLE = "role"
    RULE = "rule"
    

class IDic(ABC):
    
    def __init__(self, name: str):
        self._name = name
        self._lines: list[dict[str, Any]] = []

    @property
    def name(self):
        return self._name

    @property
    def lines(self):
        return self._lines

    def load_xl(self, path: Path, sheet_nm: str) -> None:
        """Read an excel file containing the data to load into dic."""
        
        VARS: Final[dict[str, Any]] = {
        "table_nm": str, "name":str, "is_skipped":bool, "role":str, "rule":str
        }
        
        # NOTE: Important to specify the dtypes for excel.
        # Otherwise problem, e.g. with the activ field which will not be interpreted as boolean
        
        data = pd.read_excel(io=path, sheet_name=sheet_nm, dtype=VARS)
        msg = f"The excel data for dic '{self.name}' is empty."
        assert not data.empty, msg
        
        is_subset = set(VARS.keys()).issubset(data.columns)
        if not is_subset:
            msg = f"Required column names for dic '{self.name}' are missing."
            raise ValueError(msg)
        
        EMPTY_STR: Final[str] = ""
        # NOTE: Remove NaN put by pandas. Not sure this is necessary anymore since using xl_dtypes above.  Keep it.
        for var in VARS.keys():
            data[var] = data[var].fillna(EMPTY_STR)
            
        the_lines = data.to_dict(orient='records')
        self._lines=the_lines
        
    
    def get_attributes(self, names: list[str], attr_name:str, keep_list: bool = False) -> dic_output:
        NAME: Final[str]="name"
        out: list[dict[str, Any]] = [{line[NAME]: line[attr_name]} for line in self._lines if line[NAME] in names]
        if not len(out):
            msg: str= f"No '{attr_name}' attribute available for '{names}'."
            raise KeyError(msg)
        if not keep_list and len(out) == 1:
            return out[0]
        return out
    
    def match_tag(self, tag: str, text:str)-> bool:
        a_match = re.search(pattern=rf"\b{text}\b", string=tag)
        return a_match is not None
    
    def get_names_by_attr(self, value: str, type:str, keep_list: bool = False)-> dic_output:
        NAME: Final[str]="name"
        
        out: list[dict[str, Any]] = [{line[NAME]: line[type]} for line in self._lines if self.match_tag(tag=line[type].value, text=value)]
        if not len(out):
            msg: str= f"No item found with attribute '{value}'."
            raise KeyError(msg)
        if not keep_list and len(out) == 1:
            return out[0]
        return out
        
    
    def get_roles(self, role:str, keep_list: bool = False)-> dic_output:
        attr_type: str = AttrType.ROLE.value
        out=self.get_names_by_attr(value=role, type=attr_type, keep_list=keep_list)
        return out
    
    def get_rules(self, rule:str, keep_list: bool = False)-> dic_output:
        attr_type: str = AttrType.RULE.value
        out=self.get_names_by_attr(value=rule, type=attr_type, keep_list=keep_list)
        return out
    

    # def get_role(self, name: str, keep_list: bool = False) -> str | list[str]:
    #     out = []
    #     for attr in self.attrs:
    #         # print("pattern:", rf"\b{name}\b", "role:", attr.role)
    #         if attr.role:
    #             a_match = re.search(pattern=rf"\b{name}\b", string=attr.role)
    #             if a_match is not None:
    #                 out.append(attr.name)
    #     if not len(out):
    #         msg: str = f"No item found for role '{name}'."
    #         raise KeyError(msg)
    #     if not keep_list and len(out) == 1:
    #         out = out[0]
    #     return out

    # def get_rule(self, name: str, keep_list: bool = False) -> str | list[str]:
    #     out = []
    #     for attr in self.attrs:
    #         if attr.rule:
    #             a_match = re.search(pattern=rf"\b{name}\b", string=attr.rule)
    #             if a_match is not None:
    #                 out.append(attr.name)
    #     if not len(out):
    #         msg: str = f"No item found for rule '{name}'."
    #         raise KeyError(msg)
    #     if not keep_list and len(out) == 1:
    #         out = out[0]
    #     return out