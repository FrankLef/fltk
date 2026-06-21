"""Test the richmsg.py module."""

from fltk.rich.print_msg import create_msg


def test_msg_info():
    text = "This is an information"
    target = "[cyan]" + " ".join(["\u2139 ", text]) + "[/cyan]"
    out = create_msg(text=text, type="info")
    assert out == target


def test_msg_process():
    text = "Processing something"
    target = "[dark_orange]" + " ".join(["", text]) + "[/dark_orange]"
    out = create_msg(text=text, type="process")
    assert out == target
