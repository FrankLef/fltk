from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING, Iterable, Any

if TYPE_CHECKING:
    from .main import IDic  # Only imported when checking types


def get_tags(tag_text: str | None, sep: str = chr(126)) -> dict[str, Any] | None:
    if tag_text is not None:
        # NOTE: Must use a special separator not a comma because commas are found in sub text. e.g. mask="{:,.2f}"
        try:
            tags = dict(item.split("=") for item in tag_text.split(sep))
        except ValueError:
            return None
    else:
        return None
    return tags


def get_tags_default(
    inst: IDic,
    names: Iterable[str] | None,
    group: str,
    attr_nm: str,
    default: dict[str, Any],
    na: str = "_na",
    sep: str = chr(126),
) -> dict[str, Any] | None:
    attr_dict: dict[str, Any] = {}
    tags = inst.get_attributes(names=names, group=group, attr_nm=attr_nm)
    for name, tag_text in tags.items():
        # tag_text: str = list(tag.values())[0]
        if tag_text != na:
            tag = get_tags(tag_text, sep=sep)
            # attr_dict = get_tags(tag_text, sep=sep)
            attr_dict[name] = tag
        else:
            attr_dict[name] = default
    return attr_dict
