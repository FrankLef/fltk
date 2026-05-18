from typing import NamedTuple


class DirSpecs(NamedTuple):
    """The directory specifications."""

    priority: int
    name: str
    dir: str
    emo: str
    song: str
