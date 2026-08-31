from pathlib import Path
import re
from importlib import import_module
import sys
from loguru import logger

from .scripts import get_files, get_jobs
from .utils import ring_error, ring_success
from . import utils

logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level>",
)


class JobFlow:
    def __init__(
        self,
        project_path: Path,
        work_dirs: list[str],
        *,
        job_prefix: str = "job",
        run_prefix: str = "run",
    ):
        self.project_path = project_path
        self.work_dirs = work_dirs
        self.work_path = project_path.joinpath(*work_dirs)
        self.job_prefix = job_prefix
        self.run_prefix = run_prefix

    def execute(self, job_args: str, file_pat: str | None = None) -> None:
        parsed_jobs = self.parse_jobs(job_args)
        jobs = get_jobs(
            parsed_jobs, work_path=self.work_path, job_prefix=self.job_prefix
        )
        files = get_files(jobs, file_pat=file_pat, run_prefix=self.run_prefix)
        self.run_jobs(files)

    def parse_jobs(self, jobs_args: str) -> list[str]:
        """Parse the job argument from the CLI."""
        jobs = re.sub(r"\s+", repl="", string=jobs_args)
        parsed_jobs: list[str] = list(set(jobs.lower().split(sep=",")))
        if not len(parsed_jobs):
            msg = f"The job arguments '{jobs_args}' is empty."
            raise ValueError(msg)
        return parsed_jobs

    def run_jobs(self, job_files: dict[str, list[Path]]) -> None:
        """Loop through jobs and execute the scrips."""
        njobs: int = 0
        nruns: int = 0
        for job_name, files in job_files.items():
            logger.debug(f"Job '{job_name}' with {len(files)} runs.")
            for file in files:
                self.run_module(file)
                nruns += 1
            njobs += 1
            logger.success(f"{nruns} runs in {njobs} jobs completed.")
            ring_success()

    def run_module(self, file: Path) -> None:
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
                ring_error()
                raise
