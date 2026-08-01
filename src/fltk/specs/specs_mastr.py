import polars as pl

from .base import SpecsVar
from .specs import Specs


class SpecsMastr:
    def __init__(self, name: str):
        self.name = name
        self.coll: dict[str, Specs] = {}

    def __repr__(self):
        # !r to use the repr() version of the variable (adds quotes)
        msg = f"SpecsMastr(name={self.name!r})"
        return msg

    def __str__(self):
        msg = f"{self.nspecs} specs in the {self.name} specs master"
        return msg

    @property
    def specs_nms(self) -> tuple[str, ...]:
        nms = tuple(self.coll.keys())
        return nms

    @property
    def nspecs(self) -> int:
        return len(self.coll)

    @property
    def empty(self) -> bool:
        return not self.coll

    def append(self, specs_nm: str, data: pl.DataFrame):
        reserved_nms = [x.value for x in SpecsVar]
        missing_nms = [x for x in reserved_nms if x not in data.columns]
        if missing_nms:
            msg = f"{len(missing_nms)} required columns missing\n{missing_nms}"
            raise KeyError(msg)
        not_skipped_data = data.filter(~pl.col(SpecsVar.SKIPPED)).drop(SpecsVar.SKIPPED)
        if not_skipped_data.is_empty():
            msg = f"The specs '{specs_nm}', after `skipped`, is empty!"
            raise ValueError(msg)
        specs = Specs(specs_nm, df=not_skipped_data)
        self.coll[specs_nm] = specs

    def specs(self, specs_nm: str) -> Specs:
        try:
            a_specs = self.coll[specs_nm]
        except KeyError as e:
            e.add_note(
                f"'{specs_nm}' is an invalid specs name in specs master '{self.name}'."
            )
            raise
        return a_specs
