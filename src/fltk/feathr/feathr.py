from pathlib import Path
import polars as pl
from collections.abc import Sequence
from rich import print as rprint


class Feathr:
    def __init__(self, path: Path, names: Sequence[str]) -> None:
        self.path = path
        self.names: tuple[str, ...] = tuple(sorted(list(names)))

    def __repr__(self) -> str:
        # !r to use the repr() version of the variable (adds quotes)
        msg: str = f"Feathr(path={self.path}, names={self.names})"
        return msg

    def __str__(self) -> str:
        msg: str = f"{len(self.names)} names in the feather"
        return msg

    def file(self, name: str) -> Path:
        name = name.lower()
        if name in self.names:
            path = self.path.joinpath(f"{name}.feather")
        else:
            raise ValueError(f"'{name}' is an invalid feather name.")
        return path

    def save(self, data: pl.DataFrame, name: str, silent: bool = False) -> Path:
        path = self.file(name)
        data.write_ipc(path)
        # this is megabytes ("MB"), not megabit ("Mb")
        size = data.estimated_size("mb")
        if not silent:
            msg: str = f"Save '{name}' to feather {size:.2f} MB"
            rprint(msg)
        return path

    def load(self, name: str, silent: bool = False) -> pl.DataFrame:
        path = self.file(name)
        with open(path, "rb") as f:
            data = pl.read_ipc(f)
        if not silent:
            msg: str = f"Load '{name}' from feather {data.shape}"
            rprint(msg)
        return data

    def to_dict(self) -> dict[str, pl.DataFrame]:
        out = {name: self.load(name, silent=True) for name in self.names}
        return out

    def describe(self, name: str) -> pl.DataFrame:
        data = self.load(name, silent=True)
        desc_df = data.describe()
        transp_df = desc_df.transpose(include_header=True, header_name="statistic")
        new_headers = transp_df.row(0)
        mapping = {old: new for old, new in zip(transp_df.columns, new_headers)}
        # Rename columns and drop the first row
        final_df = transp_df.rename(mapping).slice(1)
        return final_df

    def glimpse(self, name: str, max_items_per_column: int = 3) -> None:
        data = self.load(name, silent=True)
        return data.glimpse(max_items_per_column=max_items_per_column)

    def schema(self, name: str) -> pl.Schema:
        data = self.load(name, silent=True)
        return data.schema
