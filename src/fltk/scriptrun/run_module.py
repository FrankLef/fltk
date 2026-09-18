from pathlib import Path
from importlib import import_module

from . import utils


def run_module(job_name: str, file: Path) -> None:
    a_script = file.stem
    job_dir = file.parent.name
    modul = import_module(name="." + a_script, package=job_dir)
    utils.print_process(modul_nm=modul.__name__, modul_doc=modul.__doc__)
    modul.main()
