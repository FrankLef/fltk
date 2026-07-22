import polars as pl
from pathlib import Path
from joblib import Memory
from typing import Any
from datetime import datetime

from .specs_mastr import SpecsMastr


def fetch_specs(path: Path, prefix: str, sheet_nm: str) -> dict[str, Any]:
    pat: str = f"{prefix}*.xlsx"
    files = [file for file in path.glob(pat) if file.is_file()]
    if files:
        the_specs_files = {}
        for file in files:
            mtime = file.stat().st_mtime  # only used to validate the cache.
            specs_nm = file.stem.replace(prefix, "")
            the_specs_files[specs_nm] = [file, sheet_nm, mtime]
    else:
        msg: str = f"No file found with pattern '{pat}' in\n{path}"
        raise FileNotFoundError(msg)
    return the_specs_files


def load_specs(
    name: str,
    path: Path,
    *,
    prefix: str = "specs_",
    sheet_nm="data",
    cache_nm: str = ".specs_cache",
    clear_cache: bool = False,
) -> SpecsMastr:
    # NOTE: must do fetch_specs first to avoid creating cache when no file found. e.g. when doing tests.
    the_specs_files = fetch_specs(path=path, prefix=prefix, sheet_nm=sheet_nm)

    cache_path: Path = path.joinpath(cache_nm)
    memory = Memory(cache_path, verbose=0)

    @memory.cache
    def initialize_specs(name: str, specs_files: dict[str, Any]) -> SpecsMastr:
        print(f"Specs cache '{name}' updated {datetime.now().isoformat()}.")
        specs_mastr = SpecsMastr(name)
        for specs_nm, val in specs_files.items():
            data = pl.read_excel(val[0], sheet_name=val[1])
            specs_mastr.append(specs_nm, data=data)
        return specs_mastr

    # NOTE: clear the cache to force its update
    if clear_cache:
        initialize_specs.clear()

    specs_mastr = initialize_specs(name=name, specs_files=the_specs_files)
    return specs_mastr
