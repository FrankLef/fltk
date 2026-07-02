import pytest
from fltk.prnt.print_msg import create_msg


def test_msg_error():
    with pytest.raises(KeyError):
        create_msg(text="This is an information", type="X")


def test_msg_info():
    text = "This is an information"
    target = "[info]" + " ".join(["\u2139 ", text]) + "[/info]"
    out = create_msg(text=text, type="info")
    assert out == target


def test_msg_process():
    text = "Processing something"
    target = "[process]" + " ".join(["", text]) + "[/process]"
    out = create_msg(text=text, type="process")
    assert out == target
