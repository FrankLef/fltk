from pathlib import Path
import subprocess
import sys
import os
from loguru import logger

from .utils import ring_error


def run_subprocess(project_path: Path, file: Path) -> subprocess.CompletedProcess[str]:
    """Run a specific scrip with subprocess."""
    logger.info(file.name)
    custom_env = get_custom_env(project_path)
    module_name = get_module_name(file, project_path)

    result = subprocess.run(
        [sys.executable, "-X", "utf8", "-m", module_name],
        stdin=sys.stdin,
        stdout=sys.stdout,
        stderr=sys.stderr,
        cwd=str(project_path),
        env=custom_env,
        capture_output=False,  # do not use capture_output with stdin, stdout, stderr
        check=False,  # code below will take care of exit
        text=True,
    )

    if result.returncode:
        logger.exception(f"{file.name} in module '{module_name}'")
        ring_error()
        sys.exit(result.stderr)
    return result


def get_custom_env(project_path: Path) -> dict[str, str]:
    root_path: str = str(project_path)
    custom_env = os.environ.copy()
    custom_env["PYTHONPATH"] = (
        f"{root_path}{os.pathsep}{custom_env['PYTHONPATH']}"
        if "PYTHONPATH" in custom_env
        else root_path
    )
    return custom_env


def get_module_name(file: Path, project_path: Path) -> str:
    # module name is without '.py' extension
    file_path = file.with_suffix("")
    # relative path (i.e. relative to root_path)
    relative_path = file_path.relative_to(project_path)
    # replace backslash with dot
    module_name = str(relative_path).replace(os.sep, ".")
    return module_name
