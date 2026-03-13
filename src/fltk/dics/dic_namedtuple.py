from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING, NamedTuple, Any

if TYPE_CHECKING:
    from .dic import IDic  # Only imported when checking types


def get_namedtuple(inst: IDic, group: str) -> Any:
    specs = get_namedtuple_fields(inst, group)
    DicNamedTuple = NamedTuple(group, specs["fields"])  # type: ignore
    dic_named_tuple = DicNamedTuple(*specs["values"])
    # print("named tuple:\n", nt)
    return dic_named_tuple


def get_namedtuple_fields(inst: IDic, group: str) -> dict[str, Any]:
    lines = inst.get_by_group(group=group)
    values = [line.name for line in lines]  # type: ignore
    names = values.copy()

    names.insert(0, "name")
    values.insert(0, group)
    # print(f"names: {len(names)}\n", names)
    # print(f"values: {len(values)}\n", values)
    assert len(names) == len(values)

    dtypes = [str] * len(names)
    assert len(names) == len(dtypes)

    # NOTE: If there are are duplicated names, they will be removed here!
    fields = dict(zip(names, dtypes)).items()
    # print(f"fields: {len(fields)}\n", fields)

    check: int = len(names) - len(fields)
    if check:
        msg: str = f"There are {check} duplicated names in '{group}'."
        AssertionError(msg)

    out = {"names": names, "values": values, "fields": fields}

    return out
