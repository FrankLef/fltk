from pathlib import Path
import re
import json
from importlib import import_module

from .dirs_specs import DirSpecs
from . import config as cf
from . import utils
from . import get_files as gf


class WorkFlow:
    """The workflow to run the modules."""

    def __init__(self, root: Path, wf_path: Path, config: str = "config.json"):
        self.root_path = self.check_path(root)
        self.wf_path = self.check_path(wf_path)
        self.config_path = self.check_path(wf_path.joinpath(config), is_dir=False)
        self.load_config()

    def check_path(self, path: Path, is_dir: bool = True) -> Path:
        if is_dir:
            if not path.is_dir():
                raise NotADirectoryError(f"Invalid root directory:\n{path}")
        else:
            if not path.is_file():
                raise NotADirectoryError(f"Invalid file name:\n{path}")

        return path

    def check_name(self, name: str) -> str:
        val = str(name)
        val = val.replace(" ", "")
        if not val:
            raise ValueError("Empty name not allowed.")
        check = re.search(r"\W", string=val, flags=re.IGNORECASE)
        if check:
            raise ValueError(f"'{val}' not an allowed name.")
        return val

    def load_config(self) -> Path:
        path = self.config_path
        try:
            with open(path, "r", encoding="utf-8") as file:
                config = json.load(file)
        except FileNotFoundError:
            print("Error: The file was not found.")
        except json.JSONDecodeError:
            print("Error: The file is not a valid JSON.")

        prefix = config["prefix"]
        self.prefix = self.check_name(prefix)

        success_wav = self.wf_path.joinpath(config["success_wav"])
        self.success_wav = self.check_path(success_wav, is_dir=False)

        dirs = config["dirs"]
        sorted_dirs = cf.load_dirs(dirs=dirs)
        self.dirs: dict[str, DirSpecs] = sorted_dirs
        self.names: tuple[str, ...] = tuple(sorted_dirs.keys())

        return path

    def get_config_default_file(self, path: Path) -> None:
        """Get a copy of the default config file. Use it as a template!

        Args:
            path (Path): File name, including path, given to the config file.
        """
        cf.get_config_default_file(path=path)

    def execute(self, jobs_args: str, pat: str | None, ptype: str | None) -> None:
        """This execute the workflow."""
        self._pat = pat
        self._ptype = ptype
        self.parse_jobs(jobs_args)
        self.sequence_jobs()
        self.run_jobs()
        utils.ring_success(self.success_wav)

    def parse_jobs(self, jobs_args: str) -> None:
        """Parse the jobs from the CLI."""
        # remove all whitspace, tab, newline, etc
        jobs = re.sub(r"\s+", "", jobs_args)
        if not jobs:
            utils.ring_error()
            msg: str = f"The job arguments '{jobs_args}' is invalid."
            raise ValueError(msg)
        jobs_clean = jobs.lower().split(sep=",")
        jobs_clean = [x[:2] for x in jobs_clean]
        jobs_todo = set(jobs_clean)
        if not len(jobs_todo):
            utils.ring_error()
            msg = f"No jobs obtained from '{jobs_args}'."
            raise AssertionError(msg)
        self._jobs_todo = jobs_todo

    def sequence_jobs(self) -> None:
        """Sequence the jobs according to the established priorities."""
        jobs_todo = self._jobs_todo
        jobs_names = list(self.names)
        try:
            # NOTE: We can use index because the dictionary is sorted by priority in the load function above.
            jobs_pos = sorted([jobs_names.index(x) for x in jobs_todo])
        except ValueError:
            utils.ring_error()
            msg: str = "A job is not in the list of available jobs."
            raise ValueError(msg)
        if not jobs_pos:
            utils.ring_error()
            raise ValueError("No job found in the list of available jobs.")
        jobs_sequence = [jobs_names[pos] for pos in jobs_pos]
        self._jobs_sequence = jobs_sequence

    def get_files(self, root_path: Path, specs: DirSpecs, pat: str | None) -> list[str]:
        """Get the list of files in the folder, given a name pattern."""
        prefix = self.prefix
        the_files = gf.get_files(
            root_path=root_path, specs=specs, prefix=prefix, pat=pat
        )
        return the_files

    def run_jobs(self) -> None:
        """Run each job required by the user."""
        root_path = self.root_path
        pat = self._pat

        jobs_sequence = self._jobs_sequence
        for job in jobs_sequence:
            specs: DirSpecs = self.dirs[job]
            utils.print_run(dir=specs.dir, pat=pat, emo=specs.emo)
            the_files: list[str] = self.get_files(
                root_path=root_path, specs=specs, pat=pat
            )
            self.run_modul(job_dir=specs.dir, files=the_files)

    def run_modul(self, job_dir: str, files: list[str]) -> None:
        """Process the modules in the workflow directory with given pattern."""
        for a_file in files:
            modul = import_module(name="." + a_file, package=job_dir)
            utils.print_process(modul_nm=modul.__name__, modul_doc=modul.__doc__)
            try:
                if self._ptype is None:
                    modul.main()
                else:
                    try:
                        modul.main(ptype=self._ptype)
                    except TypeError as e:
                        err_msg = "unexpected keyword argument 'ptype'"
                        if err_msg not in str(e):
                            utils.ring_error()
                            raise

            except NotImplementedError as e:
                if str(e).lower().startswith("skip"):
                    utils.print_skip(modul.__name__)
                else:
                    utils.ring_error()
                    raise
            utils.print_complete(modul.__name__)
