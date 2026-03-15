from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING, NamedTuple, Any, Iterable

if TYPE_CHECKING:
    from .dic import IDic  # Only imported when checking types

type dic_lines = list[NamedTuple]
type dic_output = NamedTuple | list[NamedTuple]
type dic_names = str | list[str]
type dic_attrs = list[dict[str, Any]]


def get_lines_by_group(inst: IDic, group: str | None = None) -> dic_lines:
    if group is not None:
        the_lines: dic_lines = [line for line in inst._lines if line.group == group]  # type: ignore[attr-defined]
    else:
        return inst._lines
    if not len(the_lines):
        msg: str = f"No line found for group '{group}' in dic '{inst._name}'."
        raise KeyError(msg)
    return the_lines

def get_lines_by_names(
        inst: IDic, names: Iterable[str], group: str | None = None, keep_list: bool = False
    ) -> dic_output:
    group_lines = inst.get_lines_by_group(group)

    lines: dic_output = [line for line in group_lines if line.name in names]  # type: ignore[attr-defined]
    if not len(lines):
        msg: str = "No line found."
        raise KeyError(msg)
    if not keep_list and len(lines) == 1:
        return lines[0]
    return lines