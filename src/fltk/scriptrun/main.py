from pathlib import Path
import re
import sys
import time
from typing import Literal
from loguru import logger

from .scripts import get_files, get_jobs
from .utils import print_timer, ring_success
from .run_subprocess import run_subprocess
from .run_module import run_module

logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level>",
)


class ScriptRun:
    """Process scripts using `importlib` (default) or `subprocess`.

    We tested running 9 scripts in 9 different directories with `subprocess` and `importlib`. `subprocess` takes about 3.8 seconds but `importlib` takes  about 2.8 seconds to do the same. `importlib` seems to be faster.
    """

    def __init__(
        self,
        project_path: Path,
        work_dirs: list[str],
        *,
        mode: Literal["importlib", "subprocess"] = "importlib",
        dir_prefix: str = "job",
        file_prefix: str = "run",
    ):
        self.project_path = project_path
        self.work_dirs = work_dirs
        self.mode = mode.lower()
        self.work_path = project_path.joinpath(*work_dirs)
        self.dir_prefix = dir_prefix
        self.file_prefix = file_prefix

    def execute(
        self,
        job_args: str,
        file_pat: str | None = None,
        with_timer: bool = False,
    ) -> None:
        if with_timer:
            start_time = time.perf_counter()
        parsed_jobs = self.parse_jobs(job_args)
        jobs = get_jobs(
            parsed_jobs, work_path=self.work_path, dir_prefix=self.dir_prefix
        )
        files = get_files(jobs, file_pat=file_pat, file_prefix=self.file_prefix)
        self.run_jobs(files)
        if with_timer:
            print_timer(time.perf_counter() - start_time)

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
        nruns: int = 0
        for job_name, files in job_files.items():
            logger.debug(f"Directory '{job_name}' with {len(files)} files.")
            for file in files:
                if self.mode == "importlib":
                    run_module(file=file)
                elif self.mode == "subprocess":
                    run_subprocess(self.project_path, file=file)
                else:
                    msg: str = f"'{self.mode}' is an invalid scriptrun mode."
                    raise ValueError(msg)
                nruns += 1
        msg = f"{nruns} scripts in {len(job_files)} directories completed."
        logger.success(msg)
        ring_success()
