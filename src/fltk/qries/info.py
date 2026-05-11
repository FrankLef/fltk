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

    def assert_empty(self, msg: str | None = None) -> bool:
        qry: str = f"FROM {self._table_nm} LIMIT 1;"
        check: int = len(self._conn.sql(qry).fetchone())  # type: ignore
        if not check:
            if msg is None:
                msg = f"'{self._table_nm}' is empty."
            raise AssertionError(msg)
        return False
