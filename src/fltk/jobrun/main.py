from pathlib import Path
import re
import subprocess
import sys
import os
from loguru import logger

from .rings import ring_error, ring_success

logger.remove()

# Add a new handler using the standard colorized format minus {name}:{function}:{line}
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level>",
)


class JobRun:
    def __init__(
        self,
        project_path: Path,
        work_dirs: list[str],
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
        jobs = self.get_jobs(parsed_jobs)
        files = self.get_files(jobs, file_pat=file_pat)
        self.run_jobs(files)

    def parse_jobs(self, jobs_args: str) -> list[str]:
        """Parse the job argument from the CLI.

        Remove white scpaces. Make sur no duplicate name.

        Args:
            jobs_args (str): Job names separated by comma.

        Raises:
            ValueError: Job argument is empty.

        Returns:
            list[str]: Job names in a list.
        """
        jobs = re.sub(r"\s+", "", jobs_args)
        parsed_jobs: list[str] = list(set(jobs.lower().split(sep=",")))
        if not len(parsed_jobs):
            msg = f"The job arguments '{jobs_args}' is empty."
            raise ValueError(msg)
        return parsed_jobs

    def get_jobs(self, parsed_jobs: list[str]) -> dict[str, Path]:
        job_names = set(parsed_jobs)  # unique names only
        jobs = {}
        for job_name in job_names:
            pattern = re.compile(rf"^{self.job_prefix}.+_{job_name}")
            dirs = [
                path
                for path in self.work_path.rglob("*/")
                if path.is_dir() and pattern.search(path.name)
            ]
            if len(dirs) != 1:
                msg: str = f"There must be exactly 1 directory for job '{job_name}'. There is {len(dirs)}"
                raise AssertionError(msg)
            jobs[job_name] = dirs[0]
        # must sort the job by dirs!
        sorted_jobs = dict(sorted(jobs.items(), key=lambda item: item[1]))
        return sorted_jobs

    def get_files(
        self, jobs: dict[str, Path], file_pat: str | None
    ) -> dict[str, list[Path]]:
        if file_pat:
            full_pat = rf"^{self.run_prefix}.+_{file_pat}[.]py$"
        else:
            full_pat = rf"^{self.run_prefix}.+_.*[.]py$"
        pattern = re.compile(full_pat)
        job_files = {}
        for job_name, job_path in jobs.items():
            the_files = [
                file
                for file in job_path.iterdir()
                if file.is_file() and pattern.search(file.name)
            ]
            the_files.sort()
            job_files[job_name] = the_files
        return job_files

    def run_jobs(self, job_files: dict[str, list[Path]]) -> None:
        project_path = str(self.project_path)
        for job_name, files in job_files.items():
            msg: str = f"Job '{job_name}' with {len(files)} runs."
            # print(msg)
            logger.debug(msg)
            for file in files:
                logger.info(file.name)
                # 1. Clone system environment and fix PYTHONPATH
                custom_env = os.environ.copy()
                custom_env["PYTHONPATH"] = (
                    f"{project_path}{os.pathsep}{custom_env['PYTHONPATH']}"
                    if "PYTHONPATH" in custom_env
                    else project_path
                )

                # 2. Inject this script's specific data into the environment
                # Note: Environment values MUST be strings
                # custom_env.update(script_vars)

                # 3. Run the script purely by its name (no appended arguments)
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

                if result.returncode != 0:
                    ring_error()
                    # print(f"❌ {file.name} in {job_name} failed!\n{result.stderr}")
                    # msg = f"❌ {file.name} in {job_name} failed!\n{result.stderr}"
                    logger.exception(f"{file.name} in job '{job_name}'")
                    sys.exit(result.stderr)
                # print(f"✅ {file.name} finished.\n{result.stdout}")
            ring_success()
