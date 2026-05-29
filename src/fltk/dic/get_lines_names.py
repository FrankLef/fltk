from typing import NamedTuple, Iterable
import copy
import re


type dic_lines = list[NamedTuple]


def match_params(dic_text: str, text: str) -> bool:
    a_match = re.search(pattern=rf"\b{text}\b", string=dic_text)
    return a_match is not None


def get_lines(
    lines: dic_lines,
    group: str | None = None,
    role: str | None = None,
    rule: str | None = None,
) -> dic_lines:
    the_lines: dic_lines = copy.deepcopy(lines)

    if group:
        the_lines = [line for line in the_lines if line.group == group]  # type: ignore[attr-defined]
        if not the_lines:
            raise KeyError(f"'{group}' is an invalid group.")

    if role:
        the_lines = [
            line
            for line in the_lines
            if match_params(dic_text=line.role, text=role)  # type: ignore[attr-defined]
        ]

    if rule:
        the_lines = [
            line
            for line in the_lines
            if match_params(dic_text=line.rule, text=rule)  # type: ignore[attr-defined]
        ]

    if not the_lines:
        msg: str = (
            f"No lines returned with\ngroup='{group}'\nrole='{role}'\nrule='{rule}'"
        )
        raise AssertionError(msg)
    return the_lines


def get_names(
    lines: dic_lines,
    group: str | None = None,
    role: str | None = None,
    rule: str | None = None,
) -> tuple[str, ...]:
    the_lines: dic_lines = get_lines(lines, group=group, role=role, rule=rule)
    the_names: tuple[str, ...] = tuple([line.name for line in the_lines])  # type: ignore[attr-defined]
    return the_names


def get_lines_by_names(
    lines: dic_lines, group: str, names: Iterable[str] | None
) -> dic_lines:
    the_lines = get_lines(lines, group=group)
    if names:
        the_lines_by_names = [line for line in the_lines if line.name in names]  # type: ignore[attr-defined]
    else:
        the_lines_by_names = the_lines
    return the_lines_by_names
