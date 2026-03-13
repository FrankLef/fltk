from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING, NamedTuple, Any

if TYPE_CHECKING:
    from .dic import IDic  # Only imported when checking types

type dic_lines = list[NamedTuple]
type dic_output = NamedTuple | list[NamedTuple]
type dic_names = str | list[str]
type dic_attrs = list[dict[str, Any]]



def get_names_by_role(
        inst: IDic, role: str, group: str | None = None, keep_list: bool = False) -> dic_names:
    group_lines = inst.get_by_group(group)

    names: dic_names = [
        line.name  # type: ignore[attr-defined]
        for line in group_lines
        if inst.match_tag(tag=line.role, text=role)  # type: ignore[attr-defined]
    ]

    if not len(names):
        msg: str = f"No item found with role '{role}' in '{group}'."
        raise KeyError(msg)

    if not keep_list and len(names) == 1:
        return names[0]

    return names

def get_names_by_rule(
        inst: IDic, rule: str, group: str | None = None, keep_list: bool = False) -> dic_names:
    group_lines = inst.get_by_group(group)

    names: dic_names = [
        line.name  # type: ignore[attr-defined]
        for line in group_lines
        if inst.match_tag(tag=line.rule, text=rule)  # type: ignore[attr-defined]
    ]

    if not len(names):
        msg: str = f"No item found with rule '{rule}' in '{group}'."
        raise KeyError(msg)

    if not keep_list and len(names) == 1:
        return names[0]

    return names

def get_lines_by_role(
        inst: IDic, role: str, group: str | None = None, keep_list: bool = False) -> dic_output:
    # NOTE: The names must be in a list. i.e. keep_list=True
    names: list[str] = inst.get_names_by_role(
        role=role, group=group, keep_list=True
    )  # type: ignore
    lines: dic_output = inst.get_by_names(
        names=names, group=group, keep_list=keep_list
    )
    return lines

def get_lines_by_rule(
        inst: IDic, rule: str, group: str | None = None, keep_list: bool = False) -> dic_output:
    # NOTE: The names must be in a list. i.e. keep_list=True
    names: list[str] = inst.get_names_by_rule(
        rule=rule, group=group, keep_list=True
    )  # type: ignore
    lines: dic_output = inst.get_by_names(
        names=names, group=group, keep_list=keep_list
    )
    return lines