import polars as pl
from pathlib import Path
from joblib import Memory
from typing import Any
from datetime import datetime

from .main import Dicz

type DiczSpecs = dict[str, list[Any]]


def get_specs(path: Path, prefix: str = "bag_", sheet_nm: str = "data") -> DiczSpecs:
    file_nms = [file.name for file in path.glob("*.xlsx") if file.is_file()]
    specs = {}
    for file_nm in file_nms:
        fn = Path(path).joinpath(file_nm)
        mtime = fn.stat().st_mtime
        bag_nm = fn.stem.replace(prefix, "")
        specs[bag_nm] = [fn, sheet_nm, mtime]
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
