from pathlib import Path
import re


def get_jobs(
    parsed_jobs: list[str], work_path: Path, job_prefix: str
) -> dict[str, Path]:
    job_names = set(parsed_jobs)  # unique names only
    jobs = {}
    for job_name in job_names:
        pattern = re.compile(rf"^{job_prefix}.+_{job_name}")
        dirs = [
            path
            for path in work_path.rglob("*/")
            if path.is_dir() and pattern.search(path.name)
        ]
        if dirs:
            if len(dirs) != 1:
                msg: str = f"There must be exactly 1 directory for job '{job_name}' but there are {len(dirs)}."
                raise AssertionError(msg)
        else:
            msg = f"No directory found for job '{job_name}' and pattern {pattern}."
            FileNotFoundError(msg)
        jobs[job_name] = dirs[0]
    # must sort the job by dirs!
    sorted_jobs = dict(sorted(jobs.items(), key=lambda item: item[1]))
    return sorted_jobs


def get_files(
    jobs: dict[str, Path], file_pat: str | None, run_prefix: str
) -> dict[str, list[Path]]:
    if file_pat:
        pat = rf"^{run_prefix}.+_{file_pat}[.]py$"
    else:
        pat = rf"^{run_prefix}.+_.*[.]py$"
    pattern = re.compile(pat)
    job_files = {}
    for job_name, job_path in jobs.items():
        files = [
            file
            for file in job_path.iterdir()
            if file.is_file() and pattern.search(file.name)
        ]
        if not files:
            msg = f"No file found for job '{job_name}' and pattern {pat}."
            raise FileNotFoundError(msg)
        files.sort()
        job_files[job_name] = files
    return job_files
