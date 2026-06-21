from rich.console import Console


def create_msg(text: str, type: str | None = None) -> str:
    """Format a string to output to console using `rich`.

    Args:
        text (str): Text of the main body..
        type (str | None, optional): Format type. Defaults to None.

    Raises:
        ValueError: The type is invalid.

    Returns:
        str: Formatted string to use by `rich`.
    """
    if type is None:
        # if type is None, do nothing and return the text as is.
        return text
    else:
        a_type = type
        a_type = a_type.lower()

    match a_type:
        case "msg":
            fmt = ("[grey69]", " ", "[/grey69]")
        case "modul":
            # no space after symbol
            fmt = ("[gold3]", "\u2022", "[/gold3]")
        case "doc":
            fmt = ("[dim gold3]", " ", "[/dim gold3]")
        case "info":
            fmt = ("[cyan]", "\u2139 ", "[/cyan]")
        case "success":
            # no space after symbol
            fmt = ("[green]", "\u2713", "[/green]")
        case "warn":
            fmt = ("[yellow]", "\u26a0 ", "[/yellow]")
        case "fail":
            fmt = ("[red]", "\u2716 ", "[/red]")
        case "process":
            fmt = ("[dark_orange]", "", "[/dark_orange]")
        case "item":
            fmt = ("[green]", "", "[/green]")
        case _:
            raise ValueError(f"'{a_type}' is an invalid rich msg type.")

    msg = fmt[0] + " ".join([fmt[1], text]) + fmt[2]
    return msg


def print_msg(text: str, type: str | None = None) -> str:
    """Sent message to console using `rich`.

    Args:
        text (str): The text to print.
        type (str | None, optional): Format type. Defaults to None.

    Returns:
        str: Formatted string to use by `rich`.
    """
    msg = create_msg(text, type=type)
    console = Console()
    console.print(msg)
    return msg


def print_modul(
    modul, modul_type: str = "modul", doc_type: str = "doc", verbose: bool = True
) -> str:
    """Print message for module. Usually with `importlib`."""
    msg = f"Processing '{modul.__name__}' \u2026"
    msg = create_msg(msg, type=modul_type)
    if verbose & (modul.__doc__ is not None):
        msg = msg + "\n" + create_msg(modul.__doc__, type=doc_type)
    console = Console()
    console.print(msg)
    return msg
