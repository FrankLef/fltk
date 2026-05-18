from pathlib import Path
import re


from . import utils
from .dirs_specs import DirSpecs


def get_files(root_path: Path, specs: DirSpecs, prefix: str, pat: str | None) -> list[str]:
    """Get the list of files in the folder, given a name pattern."""
    full_pattern: str = get_full_pattern(prefix, pat=pat)

    wd = root_path.joinpath(specs.dir)
    if wd.exists():
        files = [item for item in wd.iterdir() if item.is_file()]
    else:
        utils.ring_error()
        raise NotADirectoryError(f"Invalid path\n{wd}")
    the_files = sorted(
        [
            fn.stem
            for fn in files
            if re.match(full_pattern, fn.name, flags=re.IGNORECASE)
        ]
    )
    if not len(the_files):
        utils.ring_error()
        msg: str = f"""
        No module found:
        path: {wd}
        pattern: {full_pattern}
        """
        raise ValueError(msg)
    return the_files

def get_full_pattern(prefix: str, pat: str | None) -> str:
        """Create the regex pattern used to filter the files."""
        if pat:
            full_pat = rf"^{prefix}.+_{pat}[.]py$"
        else:
            full_pat = rf"^{prefix}.+_.*[.]py$"
        return full_pat