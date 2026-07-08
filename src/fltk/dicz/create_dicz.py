import polars as pl
from pathlib import Path
from joblib import Memory
from typing import Any
from datetime import datetime

from .main import Dicz

type DiczSpecs = dict[str, list[Any]]


def get_specs(path: Path, prefix: str, sheet_nm: str) -> DiczSpecs:
    file_nms = [file for file in path.glob(f"{prefix}*.xlsx") if file.is_file()]
    specs = {}
    for file in file_nms:
        mtime = file.stat().st_mtime  # only used to validate the cache.
        bag_nm = file.stem.replace(prefix, "")
        specs[bag_nm] = [file, sheet_nm, mtime]
    return specs


def create_dicz(
    key: str,
    path: Path,
    prefix: str = "bag_",
    sheet_nm="data",
    cache_nm: str = ".dicz_cache",
    clear_cache: bool = False,
) -> Dicz:
    cache_path: Path = path.joinpath(cache_nm)
    memory = Memory(cache_path, verbose=0)

    @memory.cache
    def initialize_dicz(key: str, specs: DiczSpecs) -> Dicz:
        print(f"Dicz cache '{key}' updated {datetime.now().isoformat()}.")
        dicz = Dicz(key)
        for key, val in specs.items():
            data = pl.read_excel(val[0], sheet_name=val[1])
            dicz.append(key=key, data=data)
        return dicz

    specs = get_specs(path=path, prefix=prefix, sheet_nm=sheet_nm)

    # NOTE: clear the cache to force its update
    if clear_cache:
        initialize_dicz.clear()

    dicz = initialize_dicz(key=key, specs=specs)
    return dicz
