import pytest


from fltk.specs.specs import Specs
from fltk.specs.specs_group import SpecsGroup


@pytest.fixture
def a_specs(mastr1) -> Specs:
    a_specs = mastr1.specs("groups")
    return a_specs


def test_specs_name(a_specs):
    assert isinstance(a_specs, Specs)
    assert a_specs.name == "groups"


def test_group(a_specs):
    a_group = a_specs.group("entities")
    assert isinstance(a_group, SpecsGroup)


def test_err_key(a_specs):
    with pytest.raises(KeyError):
        a_specs.group("X")


def test_group_nms(a_specs):
    assert a_specs.group_nms == ("entities", "concepts", "fstypes")


def test_ngroups(a_specs):
    assert a_specs.ngroups == 3
