from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)


def get_progress_bar(transient: bool = False) -> Progress:
    """Custom progress bar using rich.

    Args:
        transient (bool, optional): False: Last refeshed display remains in the terminal. True: Make display disappear on exit. Defaults to False.

    Returns:
        Progress: Customized profress bar.

    References:
        https://timothygebhard.de/posts/richer-progress-bars-for-rich/.
    """
    return Progress(
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        BarColumn(),
        MofNCompleteColumn(),
        TextColumn("•"),
        TimeElapsedColumn(),
        TextColumn("•"),
        TimeRemainingColumn(),
        transient=transient,
    )
