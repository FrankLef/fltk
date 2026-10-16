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

    # module name is without '.py' extension
    file_path = file.with_suffix("")
    # relative path (i.e. relative to root_path)
    relative_path = os.path.relpath(file_path, root_path)
    # replace backslash with dot
    module_name = relative_path.replace(os.sep, ".")

    result = subprocess.run(
        [sys.executable, "-X", "utf8", "-m", module_name],
        stdin=sys.stdin,
        stdout=sys.stdout,
        stderr=sys.stderr,
        cwd=root_path,
        env=custom_env,
        capture_output=False,  # do not use capture_output with stdin, stdout, stderr
        check=False,
        text=True,
    )

    if result.returncode:
        logger.exception(f"{file.name} in job '{job_name}'")
        ring_error()
        sys.exit(result.stderr)
    return result
