from pathlib import Path
import re
import sys
from typing import Literal
from loguru import logger
import time

from .scripts import get_files, get_jobs
from .utils import ring_success
from .run_subprocess import run_subprocess
from .run_module import run_module

logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level>",
)


class ScriptRun:
    """Process scripts using subprocess (default) or importlib.

    Using importlib is significantly faster.
    """

    def __init__(
        self,
        project_path: Path,
        work_dirs: list[str],
        *,
        mode: Literal["subprocess", "module"] = "subprocess",
        with_timer: bool = False,
        job_prefix: str = "job",
        run_prefix: str = "run",
    ):
        self.project_path = project_path
        self.work_dirs = work_dirs
        self.mode = mode
        self.with_timer = with_timer
        self.work_path = project_path.joinpath(*work_dirs)
        self.job_prefix = job_prefix
        self.run_prefix = run_prefix

    def execute(self, job_args: str, file_pat: str | None = None) -> None:
        if self.with_timer:
            start_time = time.perf_counter()
        parsed_jobs = self.parse_jobs(job_args)
        jobs = get_jobs(
            parsed_jobs, work_path=self.work_path, job_prefix=self.job_prefix
        )
        files = get_files(jobs, file_pat=file_pat, run_prefix=self.run_prefix)
        self.run_jobs(files)
        if self.with_timer:
            exec_time = time.perf_counter() - start_time
            print(f"Execution time {exec_time:.6f} seconds.")

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
                if self.mode == "subprocess":
                    run_subprocess(self.project_path, job_name=job_name, file=file)
                elif self.mode == "module":
                    run_module(job_name, file=file)
                else:
                    raise ValueError(f"'{self.mode}' is an invalid mode.")
                nruns += 1
            njobs += 1
        logger.success(f"{nruns} runs in {njobs} jobs completed.")
        ring_success()
