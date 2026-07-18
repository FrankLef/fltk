import polars as pl
from pathlib import Path
from joblib import Memory
from typing import Any
from datetime import datetime

from .main import Dicz

type DiczSpecs = dict[str, list[Any]]


def get_specs(path: Path, prefix: str, sheet_nm: str) -> DiczSpecs:
    pat: str = f"{prefix}*.xlsx"
    files = [file for file in path.glob(pat) if file.is_file()]
    if files:
        specs = {}
        for file in files:
            mtime = file.stat().st_mtime  # only used to validate the cache.
            bag_nm = file.stem.replace(prefix, "")
            specs[bag_nm] = [file, sheet_nm, mtime]
    else:
        msg: str = f"No file found with pattern '{pat}' in\n{path}"
        raise FileNotFoundError(msg)
    return specs


def create_dicz(
    name: str,
    path: Path,
    *,
    prefix: str = "bag_",
    sheet_nm="data",
    cache_nm: str = ".dicz_cache",
    clear_cache: bool = False,
) -> Dicz:
    # NOTE: must do get_specs first to avoid creating cache when no file found. e.g. when doing tests.
    specs = get_specs(path=path, prefix=prefix, sheet_nm=sheet_nm)

    cache_path: Path = path.joinpath(cache_nm)
    memory = Memory(cache_path, verbose=0)

    @memory.cache
    def initialize_dicz(name: str, specs: DiczSpecs) -> Dicz:
        print(f"Dicz cache '{name}' updated {datetime.now().isoformat()}.")
        dicz = Dicz(name)
        for bag_nm, val in specs.items():
            data = pl.read_excel(val[0], sheet_name=val[1])
            dicz.append(bag_nm, data=data)
        return dicz

    # NOTE: clear the cache to force its update
    if clear_cache:
        initialize_dicz.clear()

    dicz = initialize_dicz(name=name, specs=specs)
    return dicz
