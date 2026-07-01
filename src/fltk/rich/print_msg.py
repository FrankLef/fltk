from enum import StrEnum, auto
from rich.console import Console
from rich.theme import Theme


custom_theme = Theme(
    {
        "modul": "gold3",
        "process": "dark_orange",
        "trace": "grey69",
        "debug": "dim cyan",
        "info": "cyan",
        "success": "green",
        "warn": "yellow",
        "fail": "magenta reverse",
    }
)

console = Console(theme=custom_theme)


class MsgType(StrEnum):
    PROCESS = auto()
    TRACE = auto()
    DEBUG = auto()
    INFO = auto()
    SUCCESS = auto()
    WARN = auto()
    FAIL = auto()


# Format a string to output to console using `rich`
def create_msg(text: str, type: MsgType) -> str:
    """Format a string to output to console using `rich`.

    For more standardized and formal messages used `loguru`.

    Args:
        text (str): Text to display.
        type (MsgType): Format type.

    Raises:
        ValueError: Invalid type.

    Returns:
        str: Formatted string used by `rich`.
    """
    a_type = type.lower()

    match a_type:
        case "process":
            fmt = ("[process]", "", "[/process]")
        case "trace":
            fmt = ("[trace]", " ", "[/trace]")
        case "debug":
            fmt = ("[debug]", " ", "[/debug]")
        case "info":
            fmt = ("[info]", "\u2139 ", "[/info]")
        case "success":
            # no space after symbol
            fmt = ("[success]", "\u2713", "[/success]")
        case "warn":
            fmt = ("[warn]", "\u26a0 ", "[/warn]")
        case "fail":
            fmt = ("[fail]", "\u2716 ", "[/fail]")
        case _:
            raise KeyError(f"'{a_type}' is an invalid rich msg type.")

    msg = fmt[0] + " ".join([fmt[1], text]) + fmt[2]
    return msg


def print_msg(text: str, type: MsgType) -> str:
    """Sent message to console using `rich`.

    Args:
        text (str): The text to print.
        type (str | None, optional): Format type. Defaults to None.

    Returns:
        str: Formatted string to use by `rich`.
    """
    msg = create_msg(text, type=type)
    console.print(msg)
    return msg


# def print_modul(
#     modul, modul_type: str = "modul", doc_type: str = "doc", verbose: bool = True
# ) -> str:
#     """Print message for module. Usually with `importlib`."""
#     msg = f"Processing '{modul.__name__}' \u2026"
#     msg = create_msg(msg, type=modul_type)
#     if verbose & (modul.__doc__ is not None):
#         msg = msg + "\n" + create_msg(modul.__doc__, type=doc_type)
#     console.print(msg)
#     return msg
