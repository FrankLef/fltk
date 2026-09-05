from pathlib import Path
from rich import print as rprint
import winsound

dir_path = Path(__file__).resolve().parent
SUCCESS_WAV = "kids-cartoon-close-bells-2256.wav"


def print_run(dir: str, pat: str | None, emo: str) -> None:
    """Print the run message."""
    text: str = f"\n:{emo}: Running the modules in [orchid]{dir}[/orchid]"
    if pat:
        text = text + f" with pattern [orchid]{pat}[/orchid]"
    msg = f"[cyan]{text}[/cyan]"
    rprint(msg)


def print_process(modul_nm: str, modul_doc: str | None) -> None:
    """Print the process message."""
    text = f"[cyan]Processing [orchid]{modul_nm}[/orchid][/cyan]"
    # msg = f"[cyan]\u21BB  {text}[/cyan]"
    msg = f":arrows_counterclockwise: {text}"
    rprint(msg)
    if modul_doc is not None:
        doc_msg = f"\u2139  {modul_doc}"
        rprint(doc_msg)


def print_skip(modul_nm: str) -> None:
    """Print the skip message."""
    msg = f"\u26a0[yellow]  Skip [orchid]{modul_nm}[/orchid][/yellow]"
    rprint(msg)


def print_complete(modul_nm: str) -> None:
    """Print the complete message."""
    text = f"Completed [orchid]{modul_nm}[/orchid]\n"
    msg = f"[green]\u2705 {text}[/green]"
    rprint(msg)


def print_timer(exec_time: float) -> None:
    """Print the execution time."""
    msg = f"[yellow]Execution time: [bold dark_orange]{exec_time:.3f}[/bold dark_orange] seconds.[/yellow]"
    rprint(msg)


def ring_success() -> None:
    sound_file = str(dir_path.joinpath(SUCCESS_WAV))
    winsound.PlaySound(sound_file, flags=winsound.SND_FILENAME)
    # winsound.MessageBeep(winsound.MB_ICONASTERISK)
    # winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
    # winsound.Beep(440, 500)


def ring_error() -> None:
    winsound.MessageBeep(winsound.MB_ICONHAND)
    # winsound.Beep(440, 500)
