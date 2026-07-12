import duckdb as ddb
from typing import Sequence

from ._qry_repo import QryRepo


class QryConstraints(QryRepo):
    def write_add_primary_key(self, keys: Sequence[str]) -> str:
        the_keys = ",".join(keys)
        qry = f"ALTER TABLE {self.table_nm} ADD PRIMARY KEY ({the_keys})"
        return qry

    def write_set_not_null(self, col: str) -> str:
        qry = f"ALTER TABLE {self.table_nm} ALTER COLUMN {col} SET NOT NULL"
        return qry

    def add_primary_key(self, keys: Sequence[str], skip_error: bool = False) -> None:
        qry = self.write_add_primary_key(keys)
        try:
            self.conn.sql(qry)
        except ddb.CatalogException:
            if not skip_error:
                raise
            else:
                pass
        except ddb.ConstraintException as e:
            msg: str = f"Invalid PK provided for table '{self.table_nm}'."
            e.add_note(msg)
            raise

    def set_not_null(self, cols: Sequence[str], skip_error: bool = False) -> None:
        for col in cols:
            qry = self.write_set_not_null(col)
            try:
                self.conn.sql(qry)
            except ddb.BinderException:
                if skip_error:
                    pass
                else:
                    raise
