from ._qry_repo import QryRepo


class QryInfo(QryRepo):
    @property
    def table_nm(self) -> str:
        return self._table_nm

    def count(self, where_txt: str | None = None) -> int:
        if where_txt is None:
            qry = f"SELECT count(*) FROM {self._table_nm};"
        else:
            qry = f"SELECT count(*) FROM {self._table_nm} WHERE {where_txt};"
        nrows: int = int(self._conn.sql(qry).fetchone()[0])  # type: ignore
        return nrows
