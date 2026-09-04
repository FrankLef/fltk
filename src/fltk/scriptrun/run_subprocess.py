from pathlib import Path
import subprocess
import sys
import os
from loguru import logger

from .utils import ring_error


def run_subprocess(
    project_path: Path, job_name: str, file: Path
) -> subprocess.CompletedProcess[str]:
    """Run a specific scrip with subprocess."""
    logger.info(file.name)
    root_path: str = str(project_path)
    custom_env = os.environ.copy()
    custom_env["PYTHONPATH"] = (
        f"{root_path}{os.pathsep}{custom_env['PYTHONPATH']}"
        if "PYTHONPATH" in custom_env
        else root_path
    )
    result = subprocess.run(
        [sys.executable, "-X", "utf8", file],
        stdin=sys.stdin,
        stdout=sys.stdout,
        stderr=sys.stderr,
        # capture_output=True,  # do not use capture_output with stdin, stdout, stderr
        text=True,
        env=custom_env,
    )

    if result.returncode:
        logger.exception(f"{file.name} in job '{job_name}'")
        ring_error()
        sys.exit(result.stderr)
    return result
