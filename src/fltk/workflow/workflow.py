from typing import NamedTuple, Any
from pathlib import Path
import re
import json
import shutil
from rich import print as rprint
from importlib import import_module
import winsound


class DirSpecs(NamedTuple):
    """The directory specifications."""

    priority: int
    name: str
    label: str
    dir: str
    emo: str
    song: str


class WorkFlow:
    """The workflow to run the modules."""

    def __init__(self, root: Path, wf_path: Path, config: str = "config.json"):
        self.root_path = self.check_path(root)
        self.wf_path = self.check_path(wf_path)
        self.config_path = self.check_path(wf_path.joinpath(config), is_dir=False)
        self.load_config()

    def check_path(self, path: Path, is_dir: bool = True) -> Path:
        """Validate the root_path."""
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

        prefix = config["prefix"]
        self.prefix: str = self.check_name(prefix)

        success_wav = self.wf_path.joinpath(config["success_wav"])
        self.success_wav = self.check_path(success_wav, is_dir=False)

        dirs = config["dirs"]
        self.load_dirs(dirs)

        return path

    def load_dirs(self, dirs: list[dict[str, Any]]) -> None:
        specs_dict = {}
        for dir in dirs:
            specs = DirSpecs(**dir)
            specs_dict[specs.name] = specs

        # NOTE: Must sort the dictionnary by priority.
        sorted_dirs = sorted(specs_dict.items(), key=lambda item: item[1].priority)
        sorted_dirs_dict = dict(sorted_dirs)
        self.dirs: dict[str, DirSpecs] = sorted_dirs_dict
        self.names: tuple[str, ...] = tuple(self.dirs.keys())

    def get_config_default_file(self, path: Path) -> None:
        """Get a copy of the default config file. Use it as a template!

        Args:
            path (Path): File name, including path, given to the config file.
        """
        input_path: Path = Path(__file__).parent.joinpath("wf_config.json")
        shutil.copy2(src=input_path, dst=path)
        msg: str = f"Default workflow config file copied to:\n{path}"
        rprint(msg)

    def execute(self, jobs_args: str, pat: str | None, ptype: str | None) -> None:
        """This execute the different steps of the program."""
        # self.load()
        self._pat = pat
        self._ptype = ptype
        self.parse_jobs(jobs_args)
        self.sequence_jobs()
        self.run_jobs()
        self.ring_success()

    def parse_jobs(self, jobs_args: str) -> None:
        """Parse the jobs from the CLI."""
        # remove all whitspace, tab, newline, etc
        jobs = re.sub(r"\s+", "", jobs_args)
        if not jobs:
            self.ring_error()
            msg: str = f"The job arguments '{jobs_args}' is invalid."
            raise ValueError(msg)
        jobs_clean = jobs.lower().split(sep=",")
        jobs_clean = [x[:2] for x in jobs_clean]
        jobs_todo = set(jobs_clean)
        if not len(jobs_todo):
            self.ring_error()
            msg = f"No jobs obtained from '{jobs_args}'."
            raise AssertionError(msg)
        self._jobs_todo = jobs_todo

    def sequence_jobs(self) -> None:
        """Sequence the jobs according to the established priorities."""
        jobs_todo = self._jobs_todo
        jobs_names = list(self.names)
        try:
            # NOTE: We can use index because the dictionary is sorted by priority in the load function above.
            jobs_pos = sorted([jobs_names.index(x) for x in jobs_todo])
        except ValueError:
            self.ring_error()
            msg: str = "A job is not in the list of available jobs."
            raise ValueError(msg)
        if not jobs_pos:
            self.ring_error()
            raise ValueError("No job found in the list of available jobs.")
        jobs_sequence = [jobs_names[pos] for pos in jobs_pos]
        self._jobs_sequence = jobs_sequence

    def get_full_pattern(self, pat: str | None) -> str:
        """Create the regex pattern used to filter the files."""
        if pat:
            full_pat = rf"^{self.prefix}.+_{pat}[.]py$"
        else:
            full_pat = rf"^{self.prefix}.+_.*[.]py$"
        return full_pat

    def get_files(self, root_path: Path, specs: DirSpecs, pat: str | None) -> list[str]:
        """Get the list of files in the folder, given a name pattern."""
        full_pattern: str = self.get_full_pattern(pat=pat)

        wd = root_path.joinpath(specs.dir)
        if wd.exists():
            files = [item for item in wd.iterdir() if item.is_file()]
        else:
            self.ring_error()
            raise NotADirectoryError(f"Invalid path\n{wd}")
        the_files = sorted(
            [
                fn.stem
                for fn in files
                if re.match(full_pattern, fn.name, flags=re.IGNORECASE)
            ]
        )
        if not len(the_files):
            self.ring_error()
            msg: str = f"""
            No module found:
            path: {wd}
            pattern: {full_pattern}
            """
            raise ValueError(msg)
        return the_files

    def run_jobs(self) -> None:
        """Run each job required by the user."""
        root_path = self.root_path
        pat = self._pat

        jobs_sequence = self._jobs_sequence
        for job in jobs_sequence:
            specs: DirSpecs = self.dirs[job]
            self.print_run(dir=specs.dir, pat=pat, emo=specs.emo)
            the_files: list[str] = self.get_files(
                root_path=root_path, specs=specs, pat=pat
            )
            self.run_modul(job_dir=specs.dir, files=the_files)

    def run_modul(self, job_dir: str, files: list[str]) -> None:
        """Process the modules in the workflow directory with given pattern."""
        for a_file in files:
            modul = import_module(name="." + a_file, package=job_dir)
            self.print_process(modul_nm=modul.__name__, modul_doc=modul.__doc__)
            try:
                if self._ptype is None:
                    modul.main()
                else:
                    try:
                        modul.main(ptype=self._ptype)
                    except TypeError as e:
                        err_msg = "unexpected keyword argument 'ptype'"
                        if err_msg not in str(e):
                            self.ring_error()
                            raise

            except NotImplementedError as e:
                if str(e).lower().startswith("skip"):
                    self.print_skip(modul.__name__)
                else:
                    self.ring_error()
                    raise
            self.print_complete(modul.__name__)

    def print_run(self, dir: str, pat: str | None, emo: str) -> str:
        """Print the run message."""
        text: str = f"\n:{emo}: Running the modules in [orchid]{dir}[/orchid]"
        if pat:
            text = text + f" with pattern [orchid]{pat}[/orchid]"
        msg = f"[cyan]{text}[/cyan]"
        rprint(msg)
        return msg

    def print_process(self, modul_nm: str, modul_doc: str | None) -> str:
        """Print the process message."""
        text = f"[cyan]Processing [orchid]{modul_nm}[/orchid][/cyan]"
        # msg = f"[cyan]\u21BB  {text}[/cyan]"
        msg = f":arrows_counterclockwise: {text}"

        rprint(msg)
        if modul_doc is not None:
            doc_msg = f"\u2139  {modul_doc}"
            rprint(doc_msg)
        return msg

    def print_skip(self, modul_nm: str) -> str:
        """Print the skip message."""
        msg = f"\u26a0[yellow]  Skip [orchid]{modul_nm}[/orchid][/yellow]"
        rprint(msg)
        return msg

    def print_complete(self, modul_nm: str) -> str:
        """Print the complete message."""
        text = f"Completed [orchid]{modul_nm}[/orchid]\n"
        msg = f"[green]\u2705 {text}[/green]"
        rprint(msg)
        return msg

    def ring_success(self) -> None:
        sound_file = self.success_wav
        winsound.PlaySound(str(sound_file), flags=winsound.SND_FILENAME)
        # winsound.MessageBeep(winsound.MB_ICONASTERISK)
        # winsound.Beep(440, 500)

    def ring_error(self) -> None:
        winsound.MessageBeep(winsound.MB_ICONHAND)
        # winsound.Beep(440, 500)
