"""Test the dic class."""

import pytest
from pathlib import Path

from fltk.dicz.create_dicz import create_dicz


@pytest.fixture
def path():
    return Path(__file__).parent.joinpath("fixtures")


def test_create(path) -> None:
    key: str = "dicz_test1"
    dicz = create_dicz(key, path=path)
    assert dicz.key == key
    assert dicz.nbags == 2
    assert dicz.keys == ("groups", "xbr")


def test_create_err() -> None:
    path = Path(__file__).parent
    with pytest.raises(FileNotFoundError):
        create_dicz("dicz_test1", path=path)
