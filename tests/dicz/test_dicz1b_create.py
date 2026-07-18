import pytest
from pathlib import Path

from fltk.dicz.create_dicz import create_dicz


def test_create(path, name: str = "dicz_test1") -> None:
    dicz = create_dicz(name, path=path)
    assert dicz.name == name
    assert dicz.nbags == 2
    assert dicz.bag_nms == ("groups", "xbr")


def test_create_err() -> None:
    path = Path(__file__).parent
    with pytest.raises(FileNotFoundError):
        create_dicz("dicz_test1", path=path)
