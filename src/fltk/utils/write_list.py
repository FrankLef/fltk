from typing import Iterable

def write_sql(vals: Iterable[str]) -> str:
    return ",".join([f"'{x}'" for x in vals])
    
def write_csv(vals: Iterable[str]) -> str:
    return ",".join(vals)