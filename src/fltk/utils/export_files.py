import shutil
from rich import print as rprint
from typing import NamedTuple
from pathlib import Path


class XprtFile(NamedTuple):
    name: str
    skip: bool = False


class XprtDir(NamedTuple):
    name: str
    path: Path
    files: list[XprtFile]


class XprtRun:
    def __init__(self, xprt_path: Path):
        self._xprt_path = xprt_path
        self._xprts: dict[str, XprtDir] = {}
        
    @property
    def xprt_path(self) -> Path:
        return self._xprt_path
    
    def add(self, xprt_dir: XprtDir) -> None:
        self._xprts[xprt_dir.name] = xprt_dir
        
    def add_many(self, xprt_dirs: list[XprtDir]) -> None:
        for xprt_dir in xprt_dirs:
            self.add(xprt_dir)     
        
    def run(self) -> None:
        if len(self._xprts):
            for name, xprt in self._xprts.items():
                nfiles = self.export(xprt)
                msg = f"{nfiles} files exported from '{name}'."
                rprint(msg)
        else:
            raise ValueError("No file to export.")
    
    def export(self, xprt_dir: XprtDir) -> int:
        nfiles: int = 0
        msg: str = f"Exporting from\n{xprt_dir.path}\nto\n{self._xprt_path}"
        rprint(msg)
        for a_file in xprt_dir.files:
            if not a_file.skip:
                rprint(f"'{a_file.name}'")
                src_fn = xprt_dir.path.joinpath(a_file.name)
                dest_fn = self._xprt_path.joinpath(a_file.name)
                shutil.copy2(src=src_fn, dst=dest_fn)
                nfiles += 1
        if not nfiles:
            msg = f"No file exported from '{xprt_dir.name}'."
            rprint(msg)
        return nfiles