import pytest
from fltk.specs.specs import Specs


def test_specs(mastr1):
    a_specs = mastr1.specs("groups")
    assert isinstance(a_specs, Specs)


def test_nspecs(mastr1):
    assert mastr1.nspecs == 2


def test_err_key(mastr1):
    with pytest.raises(KeyError):
        mastr1.specs("X")
