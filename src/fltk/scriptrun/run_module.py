from pathlib import Path
from importlib import import_module

from . import utils


def run_module(job_name: str, file: Path) -> None:
    a_script = file.stem
    job_dir = file.parent.name
    modul = import_module(name="." + a_script, package=job_dir)
    utils.print_process(modul_nm=modul.__name__, modul_doc=modul.__doc__)
    try:
        modul.main()
    except NotImplementedError as e:
        if str(e).lower().startswith("skip"):
            utils.print_skip(modul.__name__)
        else:
            utils.ring_error()
            raise
    except Exception as e:
        e.add_note(f"{file.name} in job '{job_name}'")
        raise
