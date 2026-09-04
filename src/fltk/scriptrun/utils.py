from pathlib import Path
from rich import print as rprint
import winsound

dir_path = Path(__file__).resolve().parent
SUCCESS_WAV = "kids-cartoon-close-bells-2256.wav"


def print_run(dir: str, pat: str | None, emo: str) -> str:
    """Print the run message."""
    text: str = f"\n:{emo}: Running the modules in [orchid]{dir}[/orchid]"
    if pat:
        text = text + f" with pattern [orchid]{pat}[/orchid]"
    msg = f"[cyan]{text}[/cyan]"
    rprint(msg)
    return msg


def print_process(modul_nm: str, modul_doc: str | None) -> str:
    """Print the process message."""
    text = f"[cyan]Processing [orchid]{modul_nm}[/orchid][/cyan]"
    # msg = f"[cyan]\u21BB  {text}[/cyan]"
    msg = f":arrows_counterclockwise: {text}"

    rprint(msg)
    if modul_doc is not None:
        doc_msg = f"\u2139  {modul_doc}"
        rprint(doc_msg)
    return msg


def print_skip(modul_nm: str) -> str:
    """Print the skip message."""
    msg = f"\u26a0[yellow]  Skip [orchid]{modul_nm}[/orchid][/yellow]"
    rprint(msg)
    return msg


def print_complete(modul_nm: str) -> str:
    """Print the complete message."""
    text = f"Completed [orchid]{modul_nm}[/orchid]\n"
    msg = f"[green]\u2705 {text}[/green]"
    rprint(msg)
    return msg


def ring_success() -> None:
    sound_file = str(dir_path.joinpath(SUCCESS_WAV))
    winsound.PlaySound(sound_file, flags=winsound.SND_FILENAME)
    # winsound.MessageBeep(winsound.MB_ICONASTERISK)
    # winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
    # winsound.Beep(440, 500)


def ring_error() -> None:
    winsound.MessageBeep(winsound.MB_ICONHAND)
    # winsound.Beep(440, 500)
