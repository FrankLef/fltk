import duckdb as ddb
from typing import Iterable

from ._qry_repo import QryRepo


class QryConstraints(QryRepo):
    @property
    def table_nm(self) -> str:
        return self._table_nm

    def write_add_primary_key(self, keys: Iterable[str]) -> str:
        the_keys = ",".join(keys)
        qry = f"ALTER TABLE {self._table_nm} ADD PRIMARY KEY ({the_keys})"
        return qry

    def write_set_not_null(self, col: str) -> str:
        qry = f"ALTER TABLE {self._table_nm} ALTER COLUMN {col} SET NOT NULL"
        return qry

    def add_primary_key(self, keys: Iterable[str]) -> None:
        qry = self.write_add_primary_key(keys)
        try:
            self._conn.sql(qry)
        except ddb.ConstraintException as e:
            msg: str = f"Invalid PK provided for table '{self._table_nm}'."
            e.add_note(msg)
            raise

    def set_not_null(self, cols: Iterable[str], skip_on_error: bool = False) -> None:
        for col in cols:
            qry = self.write_set_not_null(col)
            try:
                self._conn.sql(qry)
            except ddb.BinderException:
                if skip_on_error:
                    pass
                else:
                    raise
