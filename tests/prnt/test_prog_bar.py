from fltk.prnt.prog_bar import get_progress_bar, Progress


def test_prog_bar():
    prog_bar = get_progress_bar()
    assert isinstance(prog_bar, Progress)
