import pytest
from typing import NamedTuple


from fltk.dicz.group import DiczGroup


@pytest.fixture
def a_group(dicz1) -> DiczGroup:
    a_group = dicz1.bag("xbr").group("xbr_fstypes")
    return a_group


class FsTypeNms(NamedTuple):
    name: str
    fstype: str
    fstype_lbl: str
    fstype_en: str
    fstype_fr: str


@pytest.fixture
def fstype_nms():
    fstype_nms = FsTypeNms(
        name="xbr_fstypes",
        fstype="fstype",
        fstype_lbl="fstype_lbl",
        fstype_en="fstype_en",
        fstype_fr="fstype_fr",
    )
    return fstype_nms


def test_names_tupl(a_group, fstype_nms):
    names_tupl = a_group.names_tupl
    assert names_tupl == fstype_nms
    assert names_tupl._fields == fstype_nms._fields
