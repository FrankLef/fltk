from pathlib import Path
import re
import json
from importlib import import_module

from .dirs_specs import DirSpecs
from . import config as cfg
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

        run_prefix = config["run_prefix"]
        self.run_prefix = self.check_name(run_prefix)

        success_wav = self.wf_path.joinpath(config["success_wav"])
        self.success_wav = self.check_path(success_wav, is_dir=False)

        dirs = config["dirs"]
        sorted_dirs = cfg.load_dirs(dirs=dirs)
        self.dirs: dict[str, DirSpecs] = sorted_dirs
        self.jobs: tuple[str, ...] = tuple(sorted_dirs.keys())

        return path

    def get_config_default_file(self, path: Path) -> None:
        """Get a copy of the default config file. Use it as a template!

        Args:
            path (Path): File name, including path, given to the config file.
        """
        cfg.get_config_default_file(path=path)

    def execute(self, jobs_args: str, pat: str | None) -> None:
        """This execute the workflow."""
        self._pat = pat
        self.parse_jobs(jobs_args)
        self.run_jobs()
        utils.ring_success(self.success_wav)

    def parse_jobs(self, jobs_args: str) -> None:
        """Parse the jobs from the CLI."""
        # remove whitespace, tab, newline, etc
        jobs = re.sub(r"\s+", "", jobs_args)
        jobs_clean = set(jobs.lower().split(sep=","))
        if len(jobs_clean):
            invalid_jobs = [job for job in jobs_clean if job not in self.jobs]
            if invalid_jobs:
                msg: str = f"{len(invalid_jobs)} invalid jobs: {invalid_jobs}."
                raise KeyError(msg)
        else:
            utils.ring_error()
            msg = f"The job arguments '{jobs_args}' is empty."
            raise ValueError(msg)
        # Must sequence the jobs to do in order of priority.
        jobs_todo = tuple([job for job in self.jobs if job in jobs_clean])
        self._jobs_todo = jobs_todo

    def get_files(self, specs: DirSpecs, pat: str | None) -> list[str]:
        """Get the list of files in the folder, given a name pattern."""
        root_path = self.root_path
        run_prefix = self.run_prefix
        the_files = gf.get_files(
            root_path=root_path, specs=specs, run_prefix=run_prefix, pat=pat
        )
        return the_files

    def run_jobs(self) -> None:
        """Run each job required by the user."""
        pat = self._pat
        jobs_todo = self._jobs_todo
        for job in jobs_todo:
            specs: DirSpecs = self.dirs[job]
            utils.print_run(dir=specs.dir, pat=pat, emo=specs.emo)
            the_files: list[str] = self.get_files(specs=specs, pat=pat)
            self.run_modul(job_dir=specs.dir, files=the_files)

    def run_modul(self, job_dir: str, files: list[str]) -> None:
        """Process the modules in the workflow directory with given pattern."""
        for a_file in files:
            modul = import_module(name="." + a_file, package=job_dir)
            utils.print_process(modul_nm=modul.__name__, modul_doc=modul.__doc__)
            try:
                modul.main()
            except NotImplementedError as e:
                if str(e).lower().startswith("skip"):
                    utils.print_skip(modul.__name__)
                else:
                    utils.ring_error()
                    raise
            utils.print_complete(modul.__name__)
