from pathlib import Path
import polars as pl
from collections.abc import Sequence

from rich import print as rprint


class Feathr:
    def __init__(self, path: Path) -> None:
        self.path = path

    def __repr__(self) -> str:
        # !r to use the repr() version of the variable (adds quotes)
        return f"Feathr(path={self.path})"

    def __str__(self) -> str:
        return f"{len(self.files)} feather files."

    @property
    def names(self) -> list[str]:
        out = [x.stem for x in self.files]
        return out

    @property
    def files(self) -> list[Path]:
        out = list(self.path.glob("*.feather"))
        return out

    def file(self, name: str) -> Path:
        name = name.lower()
        path = self.path.joinpath(f"{name}.feather")
        return path

    def save(self, data: pl.DataFrame, name: str, silent: bool = False) -> Path:
        path = self.file(name)
        data.write_ipc(path)
        # this is megabytes ("MB"), not megabit ("Mb")
        size = data.estimated_size("mb")
        if not silent:
            rprint(f"Save '{name}' to feather {size:.2f} MB")
        return path

    def load(self, name: str, silent: bool = False) -> pl.DataFrame:
        path = self.file(name)
        with open(path, "rb") as f:
            data = pl.read_ipc(f)
        if not silent:
            rprint(f"Load '{name}' from feather {data.shape}")
        return data

    def drop(self, names: Sequence[str] | None = None) -> int:
        if names:
            files = [self.file(name) for name in names]
        else:
            files = self.files
        for file in files:
            file.unlink()
        return len(files)

    def to_dict(self) -> dict[str, pl.DataFrame]:
        out = {name: self.load(name, silent=True) for name in self.names}
        return out
