from typing import Any, Final
import shutil
from pathlib import Path
from rich import print as rprint

from .dirs_specs import DirSpecs


def load_dirs(dirs: list[dict[str, Any]]) -> dict[str, DirSpecs]:
    specs_dict = {}
    for dir in dirs:
        specs = DirSpecs(**dir)
        specs_dict[specs.name] = specs

    # NOTE: Must sort the dictionnary by priority.
    sorted_dirs = sorted(specs_dict.items(), key=lambda item: item[1].priority)
    sorted_dirs_dict = dict(sorted_dirs)
    return sorted_dirs_dict


def get_config_default_file(path: Path) -> None:
    """Get a copy of the default config file. Use it as a template!

    Args:
        path (Path): File name, including path, given to the config file.
    """
    FN: Final[str] = "config_wf.json"
    input_path: Path = Path(__file__).parent.joinpath(FN)
    shutil.copy2(src=input_path, dst=path)
    msg: str = f"Default workflow config file copied to:\n{path}"
    rprint(msg)
