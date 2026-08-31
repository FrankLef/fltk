from pathlib import Path
import re
import subprocess
import sys
import os
from loguru import logger

from .scripts import get_files, get_jobs
from .rings import ring_error, ring_success

logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level>",
)


class JobRun:
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
                logger.info(file.name)
                result = self.run_command(file)
                if result.returncode:
                    logger.exception(f"{file.name} in job '{job_name}'")
                    ring_error()
                    sys.exit(result.stderr)
                nruns += 1
            njobs += 1
            logger.success(f"{nruns} runs in {njobs} jobs completed.")
            ring_success()

    def run_command(self, file: Path) -> subprocess.CompletedProcess[str]:
        """Run a specific scrip with subprocess."""
        root_path: str = str(self.project_path)
        # 1. Clone system environment and fix PYTHONPATH
        custom_env = os.environ.copy()
        custom_env["PYTHONPATH"] = (
            f"{root_path}{os.pathsep}{custom_env['PYTHONPATH']}"
            if "PYTHONPATH" in custom_env
            else root_path
        )
        # 2. Run the script purely by its name (no appended arguments)
        # "-X", "utf8" used to display utf-8 character on terminal
        # stdin, stdout, stderr allow the child process's breakpoint() to use your actual terminal.
        result = subprocess.run(
            args=[sys.executable, "-X", "utf8", file],
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr,
            # capture_output=True,  # do not use capture_output with stdin, stdout, stderr
            text=True,
            env=custom_env,
        )
        return result
