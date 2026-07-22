import pytest
from pathlib import Path

from fltk.specs.load_specs import load_specs


def test_load(path, name: str = "mastr_test1") -> None:
    mastr = load_specs(name, path=path)
    assert mastr.name == name
    assert mastr.specs_nms == ("groups", "xbr")
    assert mastr.nspecs == 2


def test_load_err() -> None:
    path = Path(__file__).parent
    with pytest.raises(FileNotFoundError):
        load_specs("mastr_test1", path=path)
