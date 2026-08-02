from pathlib import Path
import polars as pl


class Feathr:
    def __init__(self, path: Path, names: tuple[str, ...]) -> None:
        self.path = path
        self.names = names

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

    def save(self, data: pl.DataFrame, name: str) -> Path:
        path = self.file(name)
        data.write_ipc(path)
        return path

    def load(self, name: str) -> pl.DataFrame:
        path = self.file(name)
        data = pl.read_ipc(path)
        return data
