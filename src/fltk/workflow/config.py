from typing import Any
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


# Get a copy of the default config file. Use it as a template!
def get_config_default_file(path: Path, file_nm: str = "config_wf.json") -> None:
    """Get a copy of the default config file. Can be used as a template for creating a new config file.

    Args:
        path (Path): Path to copy the default config file to.
        file_nm (str, optional): Name of config file. Defaults to "config_wf.json".
    """
    input_path: Path = Path(__file__).parent.joinpath(file_nm)
    shutil.copy2(src=input_path, dst=path)
    msg: str = f"Default workflow config file copied to:\n{path}"
    rprint(msg)
