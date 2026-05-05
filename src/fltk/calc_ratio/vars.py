from typing import NamedTuple


class Raw(NamedTuple):
    groups: tuple[str, ...]
    concept: str
    value: str

    @property
    def keys(self) -> str | tuple[str, ...]:
        keys = (*self.groups, self.concept)
        return keys

    @property
    def vars(self) -> tuple[str, ...]:
        vars = (*self.keys, self.value)
        return vars


class Ratios(NamedTuple):
    concept_ratio: str
    concept_num: str
    concept_den: str
    concept_name: str
    concept_pos: str
    value_ratio: str
    value_num: str
    value_den: str

    @property
    def keys(self) -> str | tuple[str, ...]:
        return self.concept_ratio
    
    @property
    def base(self) -> str | tuple[str, ...]:
        vars: tuple[str, ...] = (
            self.concept_ratio,
            self.concept_num,
            self.concept_den,
        )
        return vars
        

    @property
    def vars(self) -> str | tuple[str, ...]:
        vars: tuple[str, ...] = (
            self.concept_ratio,
            self.concept_num,
            self.concept_den,
            self.concept_name,
            self.concept_pos,
            self.value_ratio,
            self.value_num,
            self.value_den,
        )
        return vars
