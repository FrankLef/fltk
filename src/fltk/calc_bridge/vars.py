from typing import NamedTuple

class Raw(NamedTuple):
    groups: tuple[str, ...]
    period: str
    ratio: str
    value: str
    
    @property
    def keys(self) -> tuple[str, ...]:
        keys = (*self.groups, self.period, self.ratio)
        return keys
    
    @property
    def vars(self) -> tuple[str, ...]:
        vars = (*self.keys, self.value)
        return vars
        

class Periods(NamedTuple):
    start: str
    end: str
    
class Ratios(NamedTuple):
    name: str
    num_nm: str
    den_nm: str
    
    @property
    def keys(self) -> tuple[str, ...]:
        return tuple(self.name)
    
    @property
    def vars(self) -> tuple[str, ...]:
        vars = (*self.keys, self.num_nm, self.den_nm)
        return vars
        
    
class Bridge(NamedTuple):
    from_sfx: str
    to_sfx: str
    num_val: str
    den_val: str
    price: str